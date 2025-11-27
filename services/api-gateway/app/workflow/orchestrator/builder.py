from typing import Dict, Any, List, Optional
from .engine.types import WorkflowNode, WorkflowEdge, WorkflowLevel, NodeType
from .agents.core_agents import AnalysisAgent, ExecutionAgent, VerificationAgent, RecoveryAgent, SecurityAgent


class WorkflowNodeFactory:
    """Factory for creating various types of workflow nodes"""
    
    @staticmethod
    def create_start_node(name: str = "Start", node_id: str = None) -> WorkflowNode:
        """Create a start node"""
        return WorkflowNode(
            id=node_id or f"start_{name.lower().replace(' ', '_')}",
            name=name,
            node_type=NodeType.START
        )
    
    @staticmethod
    def create_end_node(name: str = "End", node_id: str = None) -> WorkflowNode:
        """Create an end node"""
        return WorkflowNode(
            id=node_id or f"end_{name.lower().replace(' ', '_')}",
            name=name,
            node_type=NodeType.END
        )
    
    @staticmethod
    def create_analysis_node(name: str = "Analysis", agent: AnalysisAgent = None, 
                           node_id: str = None) -> WorkflowNode:
        """Create an analysis node"""
        if agent is None:
            agent = AnalysisAgent()
        
        return WorkflowNode(
            id=node_id or f"analysis_{name.lower().replace(' ', '_')}",
            name=name,
            node_type=NodeType.ANALYSIS,
            agent_ref=agent,
            params={
                "agent_type": "analysis",
                "task_priority": "high"
            }
        )
    
    @staticmethod
    def create_execution_node(name: str = "Execution", agent: ExecutionAgent = None, 
                            node_id: str = None) -> WorkflowNode:
        """Create an execution node"""
        if agent is None:
            agent = ExecutionAgent()
        
        return WorkflowNode(
            id=node_id or f"execution_{name.lower().replace(' ', '_')}",
            name=name,
            node_type=NodeType.EXECUTION,
            agent_ref=agent,
            params={
                "agent_type": "execution",
                "timeout": 30
            }
        )
    
    @staticmethod
    def create_verification_node(name: str = "Verification", agent: VerificationAgent = None, 
                               node_id: str = None) -> WorkflowNode:
        """Create a verification node"""
        if agent is None:
            agent = VerificationAgent()
        
        return WorkflowNode(
            id=node_id or f"verification_{name.lower().replace(' ', '_')}",
            name=name,
            node_type=NodeType.VERIFICATION,
            agent_ref=agent,
            params={
                "agent_type": "verification",
                "validation_rules": ["accuracy_check", "consistency_check"]
            }
        )
    
    @staticmethod
    def create_recovery_node(name: str = "Recovery", agent: RecoveryAgent = None, 
                           node_id: str = None) -> WorkflowNode:
        """Create a recovery node"""
        if agent is None:
            agent = RecoveryAgent()
        
        return WorkflowNode(
            id=node_id or f"recovery_{name.lower().replace(' ', '_')}",
            name=name,
            node_type=NodeType.RECOVERY,
            agent_ref=agent,
            params={
                "agent_type": "recovery",
                "fallback_strategies": ["retry", "rollback", "notify"]
            }
        )
    
    @staticmethod
    def create_security_node(name: str = "SecurityCheck", agent: SecurityAgent = None, 
                           node_id: str = None) -> WorkflowNode:
        """Create a security check node"""
        if agent is None:
            agent = SecurityAgent()
        
        return WorkflowNode(
            id=node_id or f"security_{name.lower().replace(' ', '_')}",
            name=name,
            node_type=NodeType.SECURITY_CHECK,
            agent_ref=agent,
            params={
                "agent_type": "security",
                "security_level": "high",
                "checks": ["auth", "validate", "scan"]
            }
        )


class WorkflowBuilder:
    """Helper to build complex workflows with many nodes and levels"""
    
    def __init__(self, engine):
        self.engine = engine
        self.factory = WorkflowNodeFactory()
    
    def build_basic_workflow(self) -> str:
        """Build a basic workflow with start, analysis, execution, verification, and end"""
        workflow_id = "basic_security_workflow"
        
        # Create nodes
        start_node = self.factory.create_start_node("Start")
        analysis_node = self.factory.create_analysis_node("Analysis")
        execution_node = self.factory.create_execution_node("Execution")
        verification_node = self.factory.create_verification_node("Verification")
        end_node = self.factory.create_end_node("End")
        
        # Register nodes
        for node in [start_node, analysis_node, execution_node, verification_node, end_node]:
            self.engine.register_node(node)
        
        # Create edges
        edges = [
            WorkflowEdge(start_node.id, analysis_node.id),
            WorkflowEdge(analysis_node.id, execution_node.id),
            WorkflowEdge(execution_node.id, verification_node.id),
            WorkflowEdge(verification_node.id, end_node.id)
        ]
        
        # Register edges
        for edge in edges:
            self.engine.register_edge(edge)
        
        # Create a level
        level = WorkflowLevel(
            id="level_basic",
            name="Basic Security Level",
            description="Basic security workflow with analysis -> execution -> verification",
            nodes=[start_node.id, analysis_node.id, execution_node.id, verification_node.id, end_node.id],
            depends_on=[]
        )
        
        self.engine.register_level(level)
        
        return workflow_id
    
    def build_advanced_workflow(self) -> str:
        """Build an advanced workflow with security checks, recovery, etc."""
        workflow_id = "advanced_security_workflow"
        
        # Create nodes for advanced workflow
        nodes = []
        
        # Level 1: Input validation and security check
        start_node = self.factory.create_start_node("Input Validation Start")
        input_validation = self.factory.create_security_node("Input Validation")
        security_check = self.factory.create_security_node("Security Check")
        level1_end = self.factory.create_end_node("Level 1 End")
        nodes.extend([start_node, input_validation, security_check, level1_end])
        
        # Level 2: Analysis and Planning
        analysis = self.factory.create_analysis_node("Deep Analysis")
        planning = self.factory.create_analysis_node("Execution Planning")
        level2_end = self.factory.create_end_node("Level 2 End")
        nodes.extend([analysis, planning, level2_end])
        
        # Level 3: Execution and Verification
        execution = self.factory.create_execution_node("Secure Execution")
        verification = self.factory.create_verification_node("Execution Verification")
        recovery = self.factory.create_recovery_node("Recovery Handler")
        level3_end = self.factory.create_end_node("Level 3 End")
        nodes.extend([execution, verification, recovery, level3_end])
        
        # Level 4: Final checks and completion
        final_check = self.factory.create_security_node("Final Security Check")
        final_verification = self.factory.create_verification_node("Final Verification")
        workflow_end = self.factory.create_end_node("Workflow Complete")
        nodes.extend([final_check, final_verification, workflow_end])
        
        # Register all nodes
        for node in nodes:
            self.engine.register_node(node)
        
        # Create edges
        edges = [
            # Level 1
            WorkflowEdge(start_node.id, input_validation.id),
            WorkflowEdge(input_validation.id, security_check.id),
            WorkflowEdge(security_check.id, level1_end.id),
            
            # Level 2
            WorkflowEdge(level1_end.id, analysis.id),
            WorkflowEdge(analysis.id, planning.id),
            WorkflowEdge(planning.id, level2_end.id),
            
            # Level 3
            WorkflowEdge(level2_end.id, execution.id),
            WorkflowEdge(execution.id, verification.id),
            WorkflowEdge(verification.id, level3_end.id),
            
            # Recovery path (alternative to verification success)
            # In a real system, this would be conditional based on verification result
            WorkflowEdge(verification.id, recovery.id, condition=lambda ctx: ctx.get('verification_failed', False)),
            WorkflowEdge(recovery.id, level3_end.id),
            
            # Level 4
            WorkflowEdge(level3_end.id, final_check.id),
            WorkflowEdge(final_check.id, final_verification.id),
            WorkflowEdge(final_verification.id, workflow_end.id),
        ]
        
        for edge in edges:
            self.engine.register_edge(edge)
        
        # Create levels
        level1 = WorkflowLevel(
            id="level_input_validation",
            name="Input Validation Level",
            description="Validate and secure incoming data",
            nodes=[start_node.id, input_validation.id, security_check.id, level1_end.id],
            depends_on=[]
        )
        
        level2 = WorkflowLevel(
            id="level_analysis",
            name="Analysis Level",
            description="Analyze data and plan execution",
            nodes=[analysis.id, planning.id, level2_end.id],
            depends_on=["level_input_validation"]
        )
        
        level3 = WorkflowLevel(
            id="level_execution",
            name="Execution Level",
            description="Execute tasks with verification and recovery",
            nodes=[execution.id, verification.id, recovery.id, level3_end.id],
            depends_on=["level_analysis"]
        )
        
        level4 = WorkflowLevel(
            id="level_finalization",
            name="Finalization Level",
            description="Final security and verification checks",
            nodes=[final_check.id, final_verification.id, workflow_end.id],
            depends_on=["level_execution"]
        )
        
        for level in [level1, level2, level3, level4]:
            self.engine.register_level(level)
        
        return workflow_id
    
    def build_200_node_workflow(self) -> str:
        """Build a complex workflow with approximately 200 nodes"""
        workflow_id = "complex_200_node_workflow"
        
        # Create 200+ nodes divided into 50+ levels
        for level_idx in range(50):
            level_id = f"level_{level_idx:02d}"
            level_name = f"Processing Level {level_idx + 1}"
            level_desc = f"Level {level_idx + 1} of complex processing workflow"
            
            # Each level gets 4-5 nodes (so about 200 nodes total)
            level_nodes = []
            
            # Each level has a start, process nodes, maybe a verification, and an end
            start_node = self.factory.create_start_node(f"Level{level_idx+1}_Start", 
                                                       node_id=f"l{level_idx:02d}_start")
            self.engine.register_node(start_node)
            level_nodes.append(start_node.id)
            
            # Add 2-4 processing nodes per level
            for proc_idx in range(2, 4):
                if level_idx % 5 == 0:  # Every 5th level includes security
                    proc_node = self.factory.create_security_node(
                        f"SecCheck_{level_idx:02d}_{proc_idx}", 
                        node_id=f"l{level_idx:02d}_sec_{proc_idx}"
                    )
                elif level_idx % 7 == 0:  # Every 7th level includes verification
                    proc_node = self.factory.create_verification_node(
                        f"Verify_{level_idx:02d}_{proc_idx}", 
                        node_id=f"l{level_idx:02d}_ver_{proc_idx}"
                    )
                else:
                    proc_node = self.factory.create_analysis_node(
                        f"Process_{level_idx:02d}_{proc_idx}", 
                        node_id=f"l{level_idx:02d}_proc_{proc_idx}"
                    )
                
                self.engine.register_node(proc_node)
                level_nodes.append(proc_node.id)
            
            end_node = self.factory.create_end_node(f"Level{level_idx+1}_End", 
                                                   node_id=f"l{level_idx:02d}_end")
            self.engine.register_node(end_node)
            level_nodes.append(end_node.id)
            
            # Create edges within this level
            edge_pairs = [(level_nodes[i], level_nodes[i+1]) for i in range(len(level_nodes)-1)]
            for src, tgt in edge_pairs:
                edge = WorkflowEdge(src, tgt)
                self.engine.register_edge(edge)
            
            # Create the level
            depends_on = []
            if level_idx > 0:
                prev_level_id = f"level_{level_idx-1:02d}"
                depends_on.append(prev_level_id)
            
            level = WorkflowLevel(
                id=level_id,
                name=level_name,
                description=level_desc,
                nodes=level_nodes,
                depends_on=depends_on
            )
            self.engine.register_level(level)
        
        return workflow_id