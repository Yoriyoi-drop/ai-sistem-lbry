"""
Implementasi multi-tier LangGraph dengan 200 node dalam 50 level
Mengikuti arsitektur besar untuk AI orchestration
"""

from typing import Dict, List, Any, Optional, Callable
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage, AnyMessage
import yaml
from pydantic import BaseModel, Field
import asyncio
import logging
from enum import Enum
import uuid
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NodeType(Enum):
    """Enum untuk tipe node dalam arsitektur"""
    AI_CORE = "ai_core"
    DATA = "data"
    COMPUTE = "compute"
    QUEUE = "queue"
    DECISION = "decision"
    CONTROL = "control"
    SECURITY = "security"

class NodeConfig(BaseModel):
    """Konfigurasi untuk node individual"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    node_type: NodeType
    level: int
    position_in_level: int
    dependencies: List[str] = Field(default_factory=list)
    max_concurrent: int = 1
    timeout: int = 30
    retry_count: int = 3

class TierConfig(BaseModel):
    """Konfigurasi untuk satu tier"""
    level: int
    nodes: List[NodeConfig]
    parallel_execution: bool = False
    threshold: float = 0.5  # threshold untuk decision nodes

class NodeResult(BaseModel):
    node_id: str
    result: Any
    level: int
    timestamp: str

def merge_results(current: List[NodeResult], update: List[NodeResult]) -> List[NodeResult]:
    """Reducer function to merge node results"""
    return current + update

def merge_execution_path(current: List[str], update: List[str]) -> List[str]:
    """Reducer function to merge execution paths"""
    return current + update

def update_current_level(current: int, update: int) -> int:
    """Reducer function to update current level - keep max level reached"""
    return max(current, update)

def update_current_node(current: str, update: str) -> str:
    """Reducer function to update current node - keep the most recent"""
    return update

def merge_errors(current: List[str], update: List[str]) -> List[str]:
    """Reducer function to merge errors"""
    return current + update

# Define the state with proper reducers for LangGraph
class State(BaseModel):
    input_data: Any = Field(default=None)
    output_data: Any = Field(default=None)
    current_level: Annotated[int, update_current_level] = 0
    current_node: Annotated[str, update_current_node] = ""
    all_node_results: Annotated[List[NodeResult], merge_results] = Field(default_factory=list)
    execution_path: Annotated[List[str], merge_execution_path] = Field(default_factory=list)
    errors: Annotated[List[str], merge_errors] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    messages: Annotated[list, add_messages] = Field(default_factory=list)

class MultiTierLangGraph:
    """
    Kelas utama untuk mengelola LangGraph dengan 200 node dalam 50 tier
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file) if config_file else self._default_config()
        self.graph = StateGraph(State)
        self.nodes: Dict[str, Callable] = {}
        self.tier_configs: List[TierConfig] = []
        self._setup_graph()
    
    def _default_config(self) -> Dict[str, Any]:
        """Setup konfigurasi default untuk 200 nodes dalam 50 levels"""
        config = {
            "total_nodes": 200,
            "total_tiers": 50,
            "nodes_per_tier": 4,
            "stages": {
                "input_processing": {"start": 1, "end": 10},
                "reasoning": {"start": 11, "end": 20},
                "execution": {"start": 21, "end": 30},
                "validation": {"start": 31, "end": 40},
                "output": {"start": 41, "end": 50}
            }
        }
        return config
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load konfigurasi dari file"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _setup_tier_configs(self):
        """Setup konfigurasi tier berdasarkan konfigurasi"""
        total_tiers = self.config["total_tiers"]
        # For testing purposes, use fewer tiers to avoid recursion issues
        # In production, you would use the actual 50 tiers but with a different connection strategy
        nodes_per_tier = self.config["nodes_per_tier"]

        for tier_idx in range(total_tiers):
            level = tier_idx + 1
            nodes = []

            # Tentukan tipe node berdasarkan level
            stage = self._get_stage_for_level(level)

            for pos in range(nodes_per_tier):
                node_type = self._get_node_type_for_stage_position(stage, pos)

                node_config = NodeConfig(
                    id=f"node_{level}_{pos}",
                    node_type=node_type,
                    level=level,
                    position_in_level=pos,
                    max_concurrent=2 if node_type == NodeType.COMPUTE else 1
                )
                nodes.append(node_config)

            # Setup parallel execution untuk beberapa stage
            parallel_execution = stage in ["reasoning", "execution", "compute"]

            tier_config = TierConfig(
                level=level,
                nodes=nodes,
                parallel_execution=parallel_execution
            )

            self.tier_configs.append(tier_config)
    
    def _get_stage_for_level(self, level: int) -> str:
        """Tentukan stage berdasarkan level"""
        stages = self.config["stages"]
        for stage_name, bounds in stages.items():
            if bounds["start"] <= level <= bounds["end"]:
                return stage_name
        return "unknown"
    
    def _get_node_type_for_stage_position(self, stage: str, position: int) -> NodeType:
        """Tentukan tipe node berdasarkan stage dan posisi"""
        # Mapping untuk setiap posisi dalam tier
        position_to_type = {
            0: NodeType.AI_CORE,
            1: NodeType.DATA,
            2: NodeType.COMPUTE,
            3: NodeType.DECISION
        }
        
        # Override untuk beberapa stage
        if stage == "input_processing":
            return NodeType.DATA if position <= 1 else NodeType.AI_CORE
        elif stage == "reasoning":
            return NodeType.AI_CORE
        elif stage == "execution":
            return NodeType.COMPUTE if position % 2 == 0 else NodeType.DECISION
        elif stage == "validation":
            return NodeType.SECURITY if position == 0 else NodeType.DECISION
        elif stage == "output":
            return NodeType.CONTROL if position == 0 else NodeType.DATA
        
        return position_to_type.get(position, NodeType.AI_CORE)
    
    def _create_node_function(self, node_config: NodeConfig) -> Callable:
        """Create function untuk node berdasarkan konfigurasi"""

        async def node_function(state: State):
            logger.info(f"Menjalankan {node_config.node_type.value} node: {node_config.id} di level {node_config.level}")

            # Simulasikan pekerjaan node
            result = await self._execute_node_logic(node_config, state)

            # Return state update sebagai dictionary untuk LangGraph
            node_result = NodeResult(
                node_id=node_config.id,
                result=result,
                level=node_config.level,
                timestamp=datetime.now().isoformat()
            )

            return {
                "all_node_results": [node_result],
                "execution_path": [node_config.id],
                "current_level": node_config.level,
                "current_node": node_config.id,
                "messages": [] # We'll skip adding custom messages for now since they need to be proper langchain messages
            }

        return node_function
    
    async def _execute_node_logic(self, node_config: NodeConfig, state) -> Any:
        """Eksekusi logika spesifik untuk setiap tipe node"""
        import random
        import time

        # Simulasikan delay untuk meniru pekerjaan nyata
        await asyncio.sleep(random.uniform(0.01, 0.1))

        # Logika berdasarkan tipe node
        if node_config.node_type == NodeType.AI_CORE:
            return {
                "type": "ai_core",
                "level": node_config.level,
                "result": f"AI reasoning selesai di level {node_config.level}",
                "timestamp": datetime.now().isoformat()
            }
        elif node_config.node_type == NodeType.DATA:
            return {
                "type": "data",
                "level": node_config.level,
                "result": f"Data processing selesai di level {node_config.level}",
                "timestamp": datetime.now().isoformat()
            }
        elif node_config.node_type == NodeType.COMPUTE:
            return {
                "type": "compute",
                "level": node_config.level,
                "result": f"Compute intensive task selesai di level {node_config.level}",
                "timestamp": datetime.now().isoformat()
            }
        elif node_config.node_type == NodeType.DECISION:
            return {
                "type": "decision",
                "level": node_config.level,
                "result": f"Decision logic selesai di level {node_config.level}",
                "next_path": random.choice(["continue", "branch", "terminate"]),
                "timestamp": datetime.now().isoformat()
            }
        elif node_config.node_type == NodeType.CONTROL:
            return {
                "type": "control",
                "level": node_config.level,
                "result": f"Control flow logic selesai di level {node_config.level}",
                "timestamp": datetime.now().isoformat()
            }
        elif node_config.node_type == NodeType.SECURITY:
            return {
                "type": "security",
                "level": node_config.level,
                "result": f"Security validation selesai di level {node_config.level}",
                "timestamp": datetime.now().isoformat()
            }
        elif node_config.node_type == NodeType.QUEUE:
            return {
                "type": "queue",
                "level": node_config.level,
                "result": f"Message queuing selesai di level {node_config.level}",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "type": "unknown",
                "level": node_config.level,
                "result": f"Unknown node type di level {node_config.level}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _setup_graph(self):
        """Setup graph dengan semua node dan hubungan antar level"""
        self._setup_tier_configs()

        # Tambahkan semua node ke graph
        for tier_config in self.tier_configs:
            for node_config in tier_config.nodes:
                node_func = self._create_node_function(node_config)
                self.graph.add_node(node_config.id, node_func)

        # Setup edges antar tier (level)
        for i in range(len(self.tier_configs) - 1):
            current_tier = self.tier_configs[i]
            next_tier = self.tier_configs[i + 1]

            # Hubungkan semua node di tier saat ini ke semua node di tier berikutnya
            for current_node in current_tier.nodes:
                for next_node in next_tier.nodes:
                    self.graph.add_edge(current_node.id, next_node.id)

        # Set entry point dan finish point
        first_nodes = self.tier_configs[0].nodes
        last_nodes = self.tier_configs[-1].nodes

        for node in first_nodes:
            self.graph.add_edge(START, node.id)

        for node in last_nodes:
            self.graph.add_edge(node.id, END)
    
    def compile(self):
        """Compile graph untuk eksekusi"""
        return self.graph.compile()
    
    def get_visualization_url(self):
        """Dapatkan URL untuk visualisasi graph (jika tersedia)"""
        try:
            # Ini hanya akan bekerja jika graph telah dikompilasi dan ada akses ke API LangGraph
            compiled_graph = self.compile()
            # Dalam implementasi nyata, ini akan mengembalikan URL ke UI LangGraph
            return "https://smith.langchain.com/hub/your-graph-id"
        except Exception as e:
            logger.error(f"Error getting visualization: {e}")
            return "Visualization not available"

# Fungsi untuk membuat aplikasi standar
def create_multi_tier_app():
    """Fungsi untuk membuat aplikasi LangGraph multi-tier"""
    app = MultiTierLangGraph()
    return app.compile()

async def run_example():
    """Run example asynchronously"""
    print("Membuat aplikasi LangGraph multi-tier...")
    app = create_multi_tier_app()

    print("Menjalankan contoh eksekusi...")
    initial_state = State(
        input_data={"message": "Ini adalah input awal untuk sistem multi-tier AI"},
        metadata={"source": "user_input", "timestamp": datetime.now().isoformat()}
    )

    try:
        # Increase recursion limit to handle the complex graph
        result = await app.ainvoke(initial_state, {"recursion_limit": 150})
        print("Eksekusi selesai!")
        print(f"Jumlah node hasil: {len(result.get('all_node_results', []))}")
        print(f"Jalur eksekusi: {result.get('execution_path', [])[:5]}... (first 5 only)")
        print(f"Level akhir: {result.get('current_level', 0)}")
        print(f"Jumlah total jalur eksekusi: {len(result.get('execution_path', []))}")
        return result
    except Exception as e:
        print(f"Error saat menjalankan aplikasi: {e}")
        return None

if __name__ == "__main__":
    # Contoh penggunaan
    import asyncio
    asyncio.run(run_example())