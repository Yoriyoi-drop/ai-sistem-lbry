# 🧠 NEXAFORGE - LANGGRAPH SIMULATION (L5 Component)

from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass
import json
import uuid
from datetime import datetime

class Node:
    """Represents a node in the graph workflow"""
    def __init__(self, name: str, func: Callable, input_keys: List[str], output_keys: List[str]):
        self.name = name
        self.func = func
        self.input_keys = input_keys
        self.output_keys = output_keys
        self.id = str(uuid.uuid4())

class Edge:
    """Represents an edge connecting two nodes"""
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

class GraphState:
    """Represents the state of the workflow graph"""
    def __init__(self, initial_state: Dict[str, Any] = None):
        self.state = initial_state or {}
        self.node_results: Dict[str, Any] = {}
        self.execution_history: List[Dict] = []
    
    def update_state(self, updates: Dict[str, Any]):
        """Update the graph state with new values"""
        self.state.update(updates)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state"""
        return self.state.copy()
    
    def add_execution_record(self, node_name: str, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        """Record node execution"""
        record = {
            "node": node_name,
            "timestamp": datetime.now().isoformat(),
            "inputs": inputs,
            "outputs": outputs
        }
        self.execution_history.append(record)

class LangGraphSimulator:
    """Simulates LangGraph functionality for workflow automation"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.graph_state: Optional[GraphState] = None
    
    def add_node(self, name: str, func: Callable, input_keys: List[str], output_keys: List[str]) -> str:
        """Add a node to the graph"""
        node = Node(name, func, input_keys, output_keys)
        self.nodes[name] = node
        return node.id
    
    def add_edge(self, source: str, target: str):
        """Add an edge between two nodes"""
        if source not in self.nodes or target not in self.nodes:
            raise ValueError(f"Either {source} or {target} node doesn't exist")
        self.edges.append(Edge(source, target))
    
    def set_entry_point(self, node_name: str):
        """Set the entry point for the graph"""
        if node_name not in self.nodes:
            raise ValueError(f"Node {node_name} doesn't exist")
        self.entry_point = node_name
    
    def execute(self, initial_state: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the graph workflow"""
        self.graph_state = GraphState(initial_state or {})
        
        # Simple execution order based on edges (in a real implementation,
        # this would handle more complex dependency resolution)
        execution_order = self._determine_execution_order()
        
        for node_name in execution_order:
            node = self.nodes[node_name]
            
            # Prepare inputs for the node
            inputs = {}
            for key in node.input_keys:
                if key in self.graph_state.state:
                    inputs[key] = self.graph_state.state[key]
            
            # Execute the node function
            try:
                outputs = node.func(inputs)
                
                # Update state with outputs
                self.graph_state.update_state(outputs)
                
                # Record execution
                self.graph_state.add_execution_record(node_name, inputs, outputs)
                
            except Exception as e:
                print(f"Error executing node {node_name}: {e}")
                raise
        
        return self.graph_state.get_state()
    
    def _determine_execution_order(self) -> List[str]:
        """Determine the order to execute nodes based on dependencies"""
        # Build dependency graph
        dependencies = {node_name: set() for node_name in self.nodes}
        dependents = {node_name: set() for node_name in self.nodes}
        
        for edge in self.edges:
            dependencies[edge.target].add(edge.source)
            dependents[edge.source].add(edge.target)
        
        # Topological sort
        result = []
        ready_nodes = [node_name for node_name, deps in dependencies.items() if not deps]
        
        while ready_nodes:
            node = ready_nodes.pop(0)
            result.append(node)
            
            # Check if dependents are ready to execute
            for dependent in dependents[node]:
                dependencies[dependent].remove(node)
                if not dependencies[dependent]:
                    ready_nodes.append(dependent)
        
        if len(result) != len(self.nodes):
            raise ValueError("Graph has cycles, cannot determine execution order")
        
        return result

# Example functions to be used in the graph
def collect_data(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Example node function to collect data"""
    print("🔍 Collecting data...")
    return {
        "raw_data": [1, 2, 3, 4, 5],
        "collection_status": "completed"
    }

def process_data(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Example node function to process data"""
    print("⚙️  Processing data...")
    raw_data = inputs.get("raw_data", [])
    processed = [x * 2 for x in raw_data]
    return {
        "processed_data": processed,
        "processing_status": "completed"
    }

def generate_report(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Example node function to generate report"""
    print("📊 Generating report...")
    processed_data = inputs.get("processed_data", [])
    total = sum(processed_data)
    return {
        "report": f"Report: Sum of processed data is {total}",
        "report_status": "completed"
    }

def create_sample_workflow():
    """Create a sample workflow using LangGraph simulator"""
    print("🧱 Creating sample LangGraph workflow...")
    
    # Create the graph
    graph = LangGraphSimulator()
    
    # Add nodes
    graph.add_node(
        "data_collector",
        collect_data,
        input_keys=[],
        output_keys=["raw_data", "collection_status"]
    )
    
    graph.add_node(
        "data_processor", 
        process_data,
        input_keys=["raw_data"],
        output_keys=["processed_data", "processing_status"]
    )
    
    graph.add_node(
        "report_generator",
        generate_report,
        input_keys=["processed_data"],
        output_keys=["report", "report_status"]
    )
    
    # Add edges
    graph.add_edge("data_collector", "data_processor")
    graph.add_edge("data_processor", "report_generator")
    
    return graph

def main():
    """Demo of LangGraph simulation"""
    print("🧱 NEXAFORGE - LANGGRAPH SIMULATION (L5 Component)")
    print("=" * 50)
    
    # Create sample workflow
    workflow = create_sample_workflow()
    
    # Execute the workflow
    print(f"\n🚀 Executing workflow...")
    result = workflow.execute({"start_value": "initial"})
    
    print(f"\n✅ Workflow execution completed!")
    print(f"Final state: {json.dumps(result, indent=2)}")
    
    # Show execution history if available
    if workflow.graph_state:
        print(f"\n📋 Execution History:")
        for record in workflow.graph_state.execution_history:
            print(f"  - {record['node']} executed at {record['timestamp']}")

if __name__ == "__main__":
    main()