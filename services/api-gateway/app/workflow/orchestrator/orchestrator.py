from typing import Dict, Any, Optional
from ..engine.engine import WorkflowEngine, WorkflowOrchestrator
from ..orchestrator.builder import WorkflowBuilder
from ..engine.types import WorkflowState, NodeStatus
from ..state.storage import state_storage
import asyncio
import logging


class MultiTierWorkflowOrchestrator:
    """Main orchestrator for managing complex multi-tier workflows"""

    def __init__(self):
        self.global_orchestrator = WorkflowOrchestrator()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.builders: Dict[str, WorkflowBuilder] = {}
    
    def create_orchestrator(self, name: str, tier: int) -> WorkflowOrchestrator:
        """Create a new workflow orchestrator for a specific tier"""
        engine_id = f"{name}_tier{tier}_engine"
        engine = self.global_orchestrator.create_engine(engine_id)
        builder = WorkflowBuilder(engine)
        self.builders[engine_id] = builder
        return self.global_orchestrator
    
    async def build_all_workflows(self):
        """Build all required workflows including the 200-node complex workflow"""
        self.logger.info("Building basic workflow...")
        builder = self.builders.get("basic_security_engine")
        if not builder:
            # Create basic engine and builder
            engine = self.global_orchestrator.create_engine("basic_security_engine")
            builder = WorkflowBuilder(engine)
            self.builders["basic_security_engine"] = builder
        
        # Build the basic workflows
        builder.build_basic_workflow()
        builder.build_advanced_workflow()
        
        self.logger.info("Building complex 200-node workflow...")
        # Create engine for complex workflow
        complex_engine = self.global_orchestrator.create_engine("complex_workflow_engine")
        complex_builder = WorkflowBuilder(complex_engine)
        self.builders["complex_workflow_engine"] = complex_builder
        
        # Build the complex workflow with 200+ nodes
        complex_builder.build_200_node_workflow()
        self.logger.info("Complex workflow with 200+ nodes built successfully!")
    
    async def execute_workflow(self, engine_id: str, workflow_id: str, 
                              context: Dict[str, Any]) -> WorkflowState:
        """Execute a workflow in a specific engine"""
        return await self.global_orchestrator.execute_workflow_in_engine(
            engine_id, workflow_id, context
        )
    
    def validate_all_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Validate all registered workflows"""
        results = {}
        
        for engine_id, engine in self.global_orchestrator.engines.items():
            is_valid, errors = engine.validate_workflow()
            results[engine_id] = {
                "valid": is_valid,
                "errors": errors,
                "node_count": len(engine.nodes),
                "edge_count": len(engine.edges),
                "level_count": len(engine.levels)
            }
        
        return results
    
    async def execute_tiered_workflow(self, tiers: Dict[int, str], 
                                     context: Dict[str, Any]) -> Dict[int, WorkflowState]:
        """Execute a workflow that spans multiple tiers"""
        results = {}
        
        for tier, workflow_id in tiers.items():
            engine_id = f"tier{tier}_engine"
            
            # If engine doesn't exist, create it and set up a basic workflow
            if engine_id not in self.global_orchestrator.engines:
                self.global_orchestrator.create_engine(engine_id)
            
            # Create workflow state
            engine = self.global_orchestrator.get_engine(engine_id)
            if engine:
                state = engine.create_workflow_state(workflow_id, context)
                
                # Validate workflow
                is_valid, errors = engine.validate_workflow()
                if not is_valid:
                    self.logger.error(f"Tier {tier} workflow validation failed: {errors}")
                    continue
                
                # Execute workflow for this tier
                try:
                    result = await engine.execute_workflow(workflow_id)
                    results[tier] = result
                    # Pass results from this tier to the next tier
                    context.update({"tier_" + str(tier): result})
                except Exception as e:
                    self.logger.error(f"Tier {tier} workflow execution failed: {str(e)}")
                    results[tier] = WorkflowState(
                        workflow_id=workflow_id,
                        current_level=0,
                        current_node="",
                        status=NodeStatus.FAILED,
                        context=context,
                        error_message=str(e)
                    )
        
        return results


# Global orchestrator instance
global_orchestrator = MultiTierWorkflowOrchestrator()


async def initialize_workflows():
    """Initialize all workflows at startup"""
    await global_orchestrator.build_all_workflows()
    
    # Validate all workflows
    validation_results = global_orchestrator.validate_all_workflows()
    for engine_id, result in validation_results.items():
        print(f"Engine {engine_id}: Valid={result['valid']}, "
              f"Nodes={result['node_count']}, Edges={result['edge_count']}, "
              f"Levels={result['level_count']}")
        if not result['valid']:
            print(f"  Errors: {result['errors']}")


# Example usage
async def main():
    """Example of how to use the workflow orchestrator"""
    await initialize_workflows()
    
    # Execute a basic workflow
    context = {
        "request_type": "security_scan",
        "target": "internal_network",
        "priority": "high"
    }
    
    try:
        result = await global_orchestrator.execute_workflow(
            "basic_security_engine", 
            "basic_workflow_example", 
            context
        )
        print(f"Workflow result: {result.status}")
    except Exception as e:
        print(f"Workflow execution failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())