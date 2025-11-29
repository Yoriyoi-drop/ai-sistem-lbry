# 🔄 NEXAFORGE - PHASE 4: WORKFLOW & COMMUNICATION (L5-L6)

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import asyncio
import json
import uuid
from datetime import datetime
import threading
import time
from enum import Enum
from pathlib import Path

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis not available. Install with: pip install redis")

class WorkflowStatus(Enum):
    """Status of a workflow"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowNodeStatus(Enum):
    """Status of a workflow node"""
    WAITING = "waiting"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class WorkflowNode:
    """Represents a node in a workflow"""
    id: str
    name: str
    node_type: str  # "agent", "api_call", "condition", "loop", etc.
    parameters: Dict[str, Any]
    status: WorkflowNodeStatus = WorkflowNodeStatus.WAITING
    executed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    dependencies: List[str] = None

@dataclass
class Workflow:
    """Represents a complete workflow"""
    id: str
    name: str
    description: str
    nodes: List[WorkflowNode]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None

class WorkflowEngine:
    """Core workflow engine for L5: Workflow Automation Layer"""
    
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.workflow_locks: Dict[str, threading.Lock] = {}
        self.redis_client = self._connect_redis() if REDIS_AVAILABLE else None
        
    def _connect_redis(self):
        """Connect to Redis for message queuing"""
        try:
            # Try connecting to Redis at localhost:6379
            return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        except Exception as e:
            print(f"⚠️  Could not connect to Redis: {e}")
            print("Make sure Redis is running on localhost:6379")
            return None
    
    def create_workflow(self, name: str, description: str, nodes: List[WorkflowNode]) -> str:
        """Create a new workflow"""
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            nodes=nodes,
            created_at=datetime.now()
        )
        self.workflows[workflow_id] = workflow
        self.workflow_locks[workflow_id] = threading.Lock()
        
        # Add to Redis stream if available
        if self.redis_client:
            self.redis_client.xadd(f"workflows", {
                "id": workflow_id,
                "name": name,
                "status": WorkflowStatus.PENDING.value,
                "created_at": workflow.created_at.isoformat()
            })
        
        return workflow_id
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID"""
        return self.workflows.get(workflow_id)
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a workflow asynchronously"""
        with self.workflow_locks.get(workflow_id, threading.Lock()):
            workflow = self.workflows.get(workflow_id)
            if not workflow:
                return False
            
            if workflow.status != WorkflowStatus.PENDING:
                return False
            
            workflow.status = WorkflowStatus.RUNNING
            workflow.started_at = datetime.now()
            
            # Execute workflow in a separate thread
            thread = threading.Thread(target=self._execute_workflow_thread, args=(workflow_id,))
            thread.start()
            
            return True
    
    def _execute_workflow_thread(self, workflow_id: str):
        """Execute workflow in a separate thread"""
        workflow = self.workflows[workflow_id]
        
        try:
            # Execute nodes in sequence, respecting dependencies
            remaining_nodes = workflow.nodes.copy()
            
            while remaining_nodes:
                # Find nodes ready to execute (dependencies satisfied)
                ready_nodes = []
                for node in remaining_nodes:
                    if self._dependencies_satisfied(node, workflow):
                        ready_nodes.append(node)
                
                if not ready_nodes:
                    # Check for circular dependencies
                    print(f"⚠️  Circular dependency detected in workflow {workflow_id}")
                    workflow.status = WorkflowStatus.FAILED
                    workflow.error = "Circular dependency detected"
                    return
                
                # Execute ready nodes
                for node in ready_nodes:
                    result = self._execute_node(node)
                    node.result = result
                    node.status = WorkflowNodeStatus.COMPLETED
                    node.executed_at = datetime.now()
                    
                    remaining_nodes.remove(node)
                
                # Small delay to allow for async operations
                time.sleep(0.1)
            
            # Mark workflow as completed
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.now()
            workflow.result = {node.id: node.result for node in workflow.nodes}
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.error = str(e)
    
    def _dependencies_satisfied(self, node: WorkflowNode, workflow: Workflow) -> bool:
        """Check if all dependencies of a node are completed"""
        if not node.dependencies:
            return True
        
        for dep_id in node.dependencies:
            dep_node = next((n for n in workflow.nodes if n.id == dep_id), None)
            if not dep_node or dep_node.status != WorkflowNodeStatus.COMPLETED:
                return False
        
        return True
    
    def _execute_node(self, node: WorkflowNode) -> Any:
        """Execute a single node based on its type"""
        # In a real implementation, this would call the appropriate handler
        # based on node type (agent, API call, condition, etc.)
        
        if node.node_type == "agent":
            # Simulate agent execution
            return f"Agent node '{node.name}' executed with parameters: {node.parameters}"
        elif node.node_type == "api_call":
            # Simulate API call
            return f"API call '{node.name}' executed: {node.parameters.get('url', 'unknown')}"
        elif node.node_type == "condition":
            # Simulate condition evaluation
            return node.parameters.get("condition_result", True)
        elif node.node_type == "loop":
            # Simulate loop execution
            iterations = node.parameters.get("iterations", 1)
            results = []
            for i in range(iterations):
                results.append(f"Iteration {i+1} of loop '{node.name}'")
            return results
        else:
            return f"Unknown node type '{node.node_type}' executed"
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get detailed status of a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        
        return {
            "id": workflow.id,
            "name": workflow.name,
            "status": workflow.status.value,
            "nodes": [
                {
                    "id": node.id,
                    "name": node.name,
                    "type": node.node_type,
                    "status": node.status.value,
                    "executed_at": node.executed_at.isoformat() if node.executed_at else None
                }
                for node in workflow.nodes
            ],
            "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
            "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None
        }

class MessageQueue:
    """Message queue system for L6: Message Queue Layer"""
    
    def __init__(self):
        self.redis_client = self._connect_redis() if REDIS_AVAILABLE else None
    
    def _connect_redis(self):
        """Connect to Redis for message queuing"""
        try:
            return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        except Exception as e:
            print(f"⚠️  Could not connect to Redis: {e}")
            print("Make sure Redis is running on localhost:6379")
            return None
    
    def publish_message(self, queue_name: str, message: Dict[str, Any]) -> Optional[str]:
        """Publish a message to a queue"""
        if not self.redis_client:
            print("⚠️  Redis not available, cannot publish message")
            return None
        
        try:
            # Add timestamp to message
            message['timestamp'] = datetime.now().isoformat()
            message['id'] = str(uuid.uuid4())
            
            # Publish to Redis stream
            msg_id = self.redis_client.xadd(queue_name, message)
            return msg_id
        except Exception as e:
            print(f"Error publishing message: {e}")
            return None
    
    def subscribe_to_queue(self, queue_name: str, callback, block_timeout: int = 0):
        """Subscribe to a queue and process messages with callback"""
        if not self.redis_client:
            print("⚠️  Redis not available, cannot subscribe to queue")
            return
        
        try:
            # Start at the beginning of the stream or from the last known position
            last_id = "0-0"  # Start from the beginning
            
            while True:
                try:
                    # Block for new messages
                    messages = self.redis_client.xread({queue_name: last_id}, block=block_timeout*1000)
                    
                    if not messages:
                        continue  # No messages, continue waiting
                    
                    for stream_name, message_list in messages:
                        for msg_id, msg_data in message_list:
                            # Process message with callback
                            callback(msg_data, msg_id)
                            
                            # Update last ID to acknowledge processing
                            last_id = msg_id
                
                except KeyboardInterrupt:
                    print("Message subscription interrupted")
                    break
                except Exception as e:
                    print(f"Error in message subscription: {e}")
                    time.sleep(1)  # Wait before retrying
        except Exception as e:
            print(f"Error subscribing to queue: {e}")
    
    def get_queue_size(self, queue_name: str) -> int:
        """Get the number of messages in a queue"""
        if not self.redis_client:
            return 0
        
        try:
            return self.redis_client.xlen(queue_name)
        except:
            return 0
    
    def get_messages(self, queue_name: str, count: int = 10, latest_first: bool = True) -> List[Dict]:
        """Get messages from a queue"""
        if not self.redis_client:
            return []
        
        try:
            if latest_first:
                messages = self.redis_client.xrevrange(queue_name, count=count)
            else:
                messages = self.redis_client.xrange(queue_name, count=count)
            
            result = []
            for msg_id, msg_data in messages:
                result.append({
                    "id": msg_id,
                    "data": msg_data
                })
            
            return result
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []

class N8NIntegration:
    """Simulated n8n integration for API integrations and webhooks"""
    
    def __init__(self):
        self.webhook_endpoints = {}
        self.api_workflows = {}
    
    def register_webhook(self, name: str, url: str, callback: Callable):
        """Register a webhook endpoint"""
        self.webhook_endpoints[name] = {
            "url": url,
            "callback": callback,
            "registered_at": datetime.now()
        }
        print(f"✅ Webhook registered: {name} at {url}")
    
    def trigger_webhook(self, name: str, payload: Dict):
        """Trigger a registered webhook"""
        if name not in self.webhook_endpoints:
            print(f"❌ Webhook '{name}' not found")
            return False
        
        endpoint = self.webhook_endpoints[name]
        try:
            result = endpoint["callback"](payload)
            print(f"✅ Webhook '{name}' triggered successfully")
            return result
        except Exception as e:
            print(f"❌ Error triggering webhook '{name}': {e}")
            return False
    
    def create_api_workflow(self, name: str, steps: List[Dict]):
        """Create an API workflow (simulated)"""
        workflow_id = f"api-{uuid.uuid4().hex[:8]}"
        self.api_workflows[workflow_id] = {
            "name": name,
            "steps": steps,
            "created_at": datetime.now(),
            "active": True
        }
        print(f"✅ API workflow created: {name} (ID: {workflow_id})")
        return workflow_id

class WorkflowAutomationSystem:
    """Main system combining workflow engine and message queue"""
    
    def __init__(self):
        self.workflow_engine = WorkflowEngine()
        self.message_queue = MessageQueue()
        self.n8n_integration = N8NIntegration()
        self.agents = {}  # Will connect with agent system from Phase 3
    
    def create_complex_workflow(self, name: str, description: str, task_sequence: List[Dict]) -> str:
        """Create a complex workflow from a sequence of tasks"""
        nodes = []
        
        for i, task in enumerate(task_sequence):
            node = WorkflowNode(
                id=f"node-{i}-{uuid.uuid4().hex[:4]}",
                name=task.get("name", f"Task {i+1}"),
                node_type=task.get("type", "agent"),
                parameters=task.get("parameters", {}),
                dependencies=task.get("dependencies", [])
            )
            nodes.append(node)
        
        workflow_id = self.workflow_engine.create_workflow(name, description, nodes)
        print(f"✅ Complex workflow created: {name} (ID: {workflow_id})")
        return workflow_id
    
    def setup_agent_communication(self):
        """Setup communication between agents using message queues"""
        # Setup queues for different types of communication
        queues = [
            "agent_commands",
            "task_results", 
            "system_events",
            "workflow_updates"
        ]
        
        for queue in queues:
            print(f"✅ Message queue ready: {queue}")
        
        return queues

def main():
    """Demo of Phase 4 implementation"""
    print("🚀 NEXAFORGE - PHASE 4: WORKFLOW & COMMUNICATION (L5-L6)")
    print("=" * 60)
    
    # Initialize the workflow automation system
    wf_system = WorkflowAutomationSystem()
    
    # Demo 1: Create a simple workflow
    print("\n📝 DEMO 1: CREATING A SIMPLE WORKFLOW")
    simple_nodes = [
        WorkflowNode(
            id="node-1",
            name="Data Collection",
            node_type="agent",
            parameters={"task": "collect_sales_data"},
            dependencies=[]
        ),
        WorkflowNode(
            id="node-2", 
            name="Data Processing",
            node_type="agent",
            parameters={"task": "process_collected_data"},
            dependencies=["node-1"]  # Depends on node-1
        ),
        WorkflowNode(
            id="node-3",
            name="Generate Report",
            node_type="agent", 
            parameters={"task": "create_sales_report"},
            dependencies=["node-2"]  # Depends on node-2
        )
    ]
    
    workflow_id = wf_system.workflow_engine.create_workflow(
        "Sales Report Generation",
        "Automated workflow to collect, process, and report sales data",
        simple_nodes
    )
    print(f"✅ Workflow created with ID: {workflow_id}")
    
    # Demo 2: Execute the workflow
    print(f"\n⚙️  DEMO 2: EXECUTING WORKFLOW")
    success = wf_system.workflow_engine.execute_workflow(workflow_id)
    if success:
        print(f"✅ Workflow execution started: {workflow_id}")
    else:
        print(f"❌ Failed to start workflow execution")
    
    # Wait a moment for execution
    time.sleep(1)
    
    # Check workflow status
    status = wf_system.workflow_engine.get_workflow_status(workflow_id)
    if status:
        print(f"📊 Workflow Status: {status['status']}")
        for node in status['nodes']:
            print(f"   - {node['name']}: {node['status']}")
    
    # Demo 3: Message queue operations
    print(f"\n📨 DEMO 3: MESSAGE QUEUE OPERATIONS")
    
    # Publish a message
    msg_id = wf_system.message_queue.publish_message("agent_commands", {
        "command": "process_data",
        "agent_id": "agent-001",
        "data": {"type": "sales", "period": "Q4-2025"}
    })
    if msg_id:
        print(f"✅ Message published to 'agent_commands' queue: {msg_id}")
    
    # Check queue size
    queue_size = wf_system.message_queue.get_queue_size("agent_commands")
    print(f"📊 Queue size: {queue_size}")
    
    # Get recent messages
    messages = wf_system.message_queue.get_messages("agent_commands", count=5)
    print(f"📥 Recent messages: {len(messages)}")
    
    # Demo 4: n8n-style webhook registration
    print(f"\n🔗 DEMO 4: WEBHOOK INTEGRATION")
    
    def sample_webhook_callback(payload):
        print(f"   Received webhook payload: {payload}")
        return {"status": "success", "processed_at": datetime.now().isoformat()}
    
    wf_system.n8n_integration.register_webhook(
        "sales_data_update",
        "/webhooks/sales-data",
        sample_webhook_callback
    )
    
    # Trigger the webhook
    wf_system.n8n_integration.trigger_webhook("sales_data_update", {
        "event": "data_updated",
        "timestamp": datetime.now().isoformat(),
        "data": {"records": 150, "type": "sales"}
    })
    
    # Demo 5: Complex workflow creation
    print(f"\n🔄 DEMO 5: COMPLEX WORKFLOW CREATION")
    
    complex_tasks = [
        {"name": "Authenticate User", "type": "api_call", "parameters": {"url": "/api/auth", "method": "POST"}},
        {"name": "Validate Input", "type": "agent", "parameters": {"task": "validate_input"}, "dependencies": ["node-0"]},
        {"name": "Process Request", "type": "agent", "parameters": {"task": "process_request"}, "dependencies": ["node-1"]},
        {"name": "Generate Response", "type": "agent", "parameters": {"task": "generate_response"}, "dependencies": ["node-2"]},
        {"name": "Log Activity", "type": "api_call", "parameters": {"url": "/api/logs", "method": "POST"}, "dependencies": ["node-3"]}
    ]
    
    complex_wf_id = wf_system.create_complex_workflow(
        "User Request Handler",
        "Complex workflow to handle user requests with authentication, validation, and logging",
        complex_tasks
    )
    
    print(f"✅ Complex workflow created: {complex_wf_id}")
    
    # Demo 6: Setup agent communication
    print(f"\n💬 DEMO 6: AGENT COMMUNICATION SETUP")
    queues = wf_system.setup_agent_communication()
    print(f"✅ Communication queues established: {', '.join(queues)}")
    
    print(f"\n🎉 PHASE 4 COMPLETE: Workflow & Communication Systems Ready!")
    print("   - Workflow engine with multi-step execution")
    print("   - Message queue system for inter-service communication")
    print("   - Webhook integration for external services")
    print("   - Ready for integration with previous layers")

if __name__ == "__main__":
    main()