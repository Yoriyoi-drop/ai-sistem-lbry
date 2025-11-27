from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import logging
from collections import defaultdict
from .types import (
    WorkflowNode, 
    WorkflowEdge, 
    WorkflowLevel, 
    WorkflowState, 
    NodeType, 
    NodeStatus
)
from ..agents.base_agent import BaseAgent
import networkx as nx


class WorkflowEngine:
    """Main workflow engine to orchestrate 200+ nodes and 50+ levels"""
    
    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: List[WorkflowEdge] = []
        self.levels: Dict[str, WorkflowLevel] = {}
        self.state_graph: nx.DiGraph = nx.DiGraph()
        self.logger = logging.getLogger(__name__)
        self.active_states: Dict[str, WorkflowState] = {}
        
    def register_node(self, node: WorkflowNode) -> None:
        """Register a node in the workflow engine"""
        self.nodes[node.id] = node
        self.state_graph.add_node(node.id, node_type=node.node_type.value)
        
    def register_edge(self, edge: WorkflowEdge) -> None:
        """Register an edge between nodes in the workflow engine"""
        self.edges.append(edge)
        # Add edge to the state graph
        self.state_graph.add_edge(edge.source_node_id, edge.target_node_id)
        
    def register_level(self, level: WorkflowLevel) -> None:
        """Register a level in the workflow engine"""
        self.levels[level.id] = level
        
    def build_workflow_from_levels(self) -> None:
        """Build workflow graph based on registered levels and dependencies"""
        for level_id, level in self.levels.items():
            for node_id in level.nodes:
                if node_id not in self.nodes:
                    raise ValueError(f"Node {node_id} referenced in level {level_id} not found")
        
        # Build the execution dependency graph
        for level in self.levels.values():
            for dep_id in level.depends_on:
                if dep_id not in self.levels:
                    raise ValueError(f"Dependency level {dep_id} not found")
    
    def create_workflow_state(self, workflow_id: str, initial_context: Dict[str, Any]) -> WorkflowState:
        """Create initial state for a new workflow execution"""
        state = WorkflowState(
            workflow_id=workflow_id,
            current_level=0,
            current_node="",
            status=NodeStatus.PENDING,
            context=initial_context,
            execution_path=[]
        )
        self.active_states[workflow_id] = state
        return state
    
    async def execute_workflow(self, workflow_id: str) -> WorkflowState:
        """Execute a workflow from start to finish"""
        if workflow_id not in self.active_states:
            raise ValueError(f"Workflow state for ID {workflow_id} not found")
        
        state = self.active_states[workflow_id]
        state.status = NodeStatus.RUNNING
        
        try:
            # Execute each level sequentially
            level_order = self._get_level_execution_order()
            
            for level_idx, level_id in enumerate(level_order):
                level = self.levels[level_id]
                state.current_level = level_idx
                
                # Execute current level
                level_results = await level.execute(state.context, self)
                
                # Update state context with level results
                for node_id, result in level_results.items():
                    if isinstance(result, dict):
                        state.context.update(result)
                
                # Update execution path
                state.execution_path.extend([f"{level_id}:{node_id}" for node_id in level.nodes])
            
            state.status = NodeStatus.COMPLETED
            state.completed_at = datetime.utcnow()
            return state
            
        except Exception as e:
            state.status = NodeStatus.FAILED
            state.error_message = str(e)
            state.completed_at = datetime.utcnow()
            self.logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            raise
    
    def get_node(self, node_id: str) -> Optional[WorkflowNode]:
        """Get a node by ID"""
        return self.nodes.get(node_id)
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get neighbors of a node in the execution graph"""
        if node_id in self.state_graph:
            return list(self.state_graph.neighbors(node_id))
        return []
    
    def get_predecessors(self, node_id: str) -> List[str]:
        """Get predecessors of a node in the execution graph"""
        if node_id in self.state_graph:
            return list(self.state_graph.predecessors(node_id))
        return []
    
    def _get_level_execution_order(self) -> List[str]:
        """Get the execution order of levels based on dependencies"""
        # Create dependency graph for levels
        level_graph = nx.DiGraph()
        
        # Add all levels to the graph
        for level_id in self.levels:
            level_graph.add_node(level_id)
        
        # Add dependency edges
        for level in self.levels.values():
            for dep in level.depends_on:
                if dep in self.levels:
                    level_graph.add_edge(dep, level.id)
        
        # Return topological sort (execution order)
        return list(nx.topological_sort(level_graph))
    
    def validate_workflow(self) -> Tuple[bool, List[str]]:
        """Validate the workflow for cycles, missing nodes, etc."""
        errors = []
        
        # Check for cycles in the state graph
        try:
            cycle = nx.find_cycle(self.state_graph)
            if cycle:
                errors.append(f"Cycle detected in workflow: {cycle}")
        except nx.NetworkXNoCycle:
            pass
        
        # Check for disconnected nodes
        if not nx.is_weakly_connected(self.state_graph):
            errors.append("Workflow contains disconnected components")
        
        # Check if each level references valid nodes
        for level_id, level in self.levels.items():
            for node_id in level.nodes:
                if node_id not in self.nodes:
                    errors.append(f"Level {level_id} references non-existent node {node_id}")
        
        # Check for valid dependencies
        for level_id, level in self.levels.items():
            for dep_id in level.depends_on:
                if dep_id not in self.levels:
                    errors.append(f"Level {level_id} depends on non-existent level {dep_id}")
        
        return len(errors) == 0, errors


class WorkflowOrchestrator:
    """Higher-level orchestrator to manage multiple workflows"""
    
    def __init__(self):
        self.engines: Dict[str, WorkflowEngine] = {}
        self.active_workflows: Dict[str, str] = {}  # workflow_id -> engine_id
        self.logger = logging.getLogger(__name__)
    
    def create_engine(self, engine_id: str) -> WorkflowEngine:
        """Create a new workflow engine instance"""
        if engine_id in self.engines:
            raise ValueError(f"Engine with ID {engine_id} already exists")
        
        engine = WorkflowEngine()
        self.engines[engine_id] = engine
        return engine
    
    def get_engine(self, engine_id: str) -> Optional[WorkflowEngine]:
        """Get a workflow engine by ID"""
        return self.engines.get(engine_id)
    
    async def execute_workflow_in_engine(self, engine_id: str, workflow_id: str, 
                                       initial_context: Dict[str, Any]) -> WorkflowState:
        """Execute a workflow in a specific engine"""
        engine = self.get_engine(engine_id)
        if not engine:
            raise ValueError(f"Engine {engine_id} not found")
        
        # Create workflow state
        state = engine.create_workflow_state(workflow_id, initial_context)
        
        # Validate workflow before execution
        is_valid, errors = engine.validate_workflow()
        if not is_valid:
            raise ValueError(f"Workflow validation failed: {errors}")
        
        # Execute workflow
        result = await engine.execute_workflow(workflow_id)
        
        return result