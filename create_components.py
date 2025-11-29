import os
from pathlib import Path

def create_additional_components():
    """Create additional UI components for the frontend"""
    frontend_dir = Path("./frontend")
    
    # Create Button component
    button_component = '''import React from 'react';

const Button = ({ children, variant = "default", size = "default", className = "", onClick, disabled = false }) => {
  const baseClasses = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50";
  
  const variantClasses = {
    default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
    destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
    outline: "border border-input bg-transparent shadow-sm hover:bg-accent hover:text-accent-foreground",
    secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
    ghost: "hover:bg-accent hover:text-accent-foreground",
    link: "text-primary underline-offset-4 hover:underline"
  };
  
  const sizeClasses = {
    default: "h-9 px-4 py-2",
    sm: "h-8 rounded-md px-3 text-xs",
    lg: "h-10 rounded-md px-8",
    icon: "h-9 w-9"
  };
  
  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;
  
  return (
    <button 
      className={classes} 
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export { Button };
'''
    
    button_path = frontend_dir / "src" / "components" / "ui" / "Button.jsx"
    button_path.parent.mkdir(exist_ok=True)
    with open(button_path, "w") as f:
        f.write(button_component)
    
    print("🔘 src/components/ui/Button.jsx created")
    
    # Create Agents page
    agents_page = '''import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Agent, Play, Square, Settings, Plus, Search } from 'lucide-react';
import { getAgents, startAgent, stopAgent } from '../services/api';

const Agents = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await getAgents();
        setAgents(data);
      } catch (error) {
        console.error('Failed to fetch agents:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  const handleStartAgent = async (agentId) => {
    try {
      await startAgent(agentId);
      // Update the agent status in the list
      setAgents(agents.map(agent => 
        agent.id === agentId ? { ...agent, status: 'running' } : agent
      ));
    } catch (error) {
      console.error('Failed to start agent:', error);
    }
  };

  const handleStopAgent = async (agentId) => {
    try {
      await stopAgent(agentId);
      // Update the agent status in the list
      setAgents(agents.map(agent => 
        agent.id === agentId ? { ...agent, status: 'stopped' } : agent
      ));
    } catch (error) {
      console.error('Failed to stop agent:', error);
    }
  };

  const filteredAgents = agents.filter(agent => 
    agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    agent.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="p-6 flex justify-center items-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">AI Agents</h1>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Create Agent
        </Button>
      </div>

      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search agents..."
            className="pl-8 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredAgents.map((agent) => (
          <Card key={agent.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Agent className="h-5 w-5" />
                    {agent.name}
                  </CardTitle>
                  <CardDescription>{agent.type}</CardDescription>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs ${
                  agent.status === 'running' ? 'bg-green-100 text-green-800' : 
                  agent.status === 'stopped' ? 'bg-red-100 text-red-800' : 
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {agent.status}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">{agent.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-sm">Tasks: {agent.task_count}</span>
                <div className="flex space-x-2">
                  {agent.status === 'stopped' ? (
                    <Button size="sm" onClick={() => handleStartAgent(agent.id)}>
                      <Play className="mr-1 h-3 w-3" />
                      Start
                    </Button>
                  ) : (
                    <Button variant="outline" size="sm" onClick={() => handleStopAgent(agent.id)}>
                      <Square className="mr-1 h-3 w-3" />
                      Stop
                    </Button>
                  )}
                  <Button variant="outline" size="sm">
                    <Settings className="h-3 w-3" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredAgents.length === 0 && (
        <div className="text-center py-12">
          <Agent className="h-12 w-12 mx-auto text-gray-400" />
          <h3 className="mt-2 text-lg font-medium">No agents</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by creating a new AI agent.
          </p>
          <div className="mt-6">
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Agent
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Agents;
'''
    
    agents_path = frontend_dir / "src" / "pages" / "Agents.jsx"
    with open(agents_path, "w") as f:
        f.write(agents_page)
    
    print("🤖 src/pages/Agents.jsx created")
    
    # Create Workflow Builder page
    workflow_page = '''import React, { useState, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Workflow, Plus, Play, Save, Copy, Trash2 } from 'lucide-react';

const WorkflowBuilder = () => {
  const [workflowName, setWorkflowName] = useState('');
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const canvasRef = useRef(null);

  const nodeTypes = [
    { id: 'start', name: 'Start', color: 'bg-green-500' },
    { id: 'end', name: 'End', color: 'bg-red-500' },
    { id: 'task', name: 'Task', color: 'bg-blue-500' },
    { id: 'condition', name: 'Condition', color: 'bg-yellow-500' },
    { id: 'api', name: 'API Call', color: 'bg-purple-500' },
  ];

  const addNode = (nodeType) => {
    const newNode = {
      id: `node_${Date.now()}`,
      type: nodeType.id,
      name: nodeType.name,
      color: nodeType.color,
      position: { x: 100, y: 100 },
      data: { label: nodeType.name }
    };
    setNodes([...nodes, newNode]);
  };

  const deleteNode = (nodeId) => {
    setNodes(nodes.filter(node => node.id !== nodeId));
    setConnections(connections.filter(conn => 
      conn.source !== nodeId && conn.target !== nodeId
    ));
    if (selectedNode?.id === nodeId) {
      setSelectedNode(null);
    }
  };

  return (
    <div className="h-screen flex flex-col">
      <div className="border-b p-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold flex items-center">
            <Workflow className="mr-2 h-5 w-5" />
            Workflow Builder
          </h1>
          <input
            type="text"
            placeholder="Workflow name"
            className="border rounded px-3 py-1 text-sm w-64"
            value={workflowName}
            onChange={(e) => setWorkflowName(e.target.value)}
          />
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Save className="mr-2 h-4 w-4" />
            Save
          </Button>
          <Button variant="outline" size="sm">
            <Copy className="mr-2 h-4 w-4" />
            Duplicate
          </Button>
          <Button size="sm">
            <Play className="mr-2 h-4 w-4" />
            Run
          </Button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <div className="w-64 border-r p-4">
          <h2 className="font-semibold mb-4">Node Library</h2>
          <div className="space-y-2">
            {nodeTypes.map((nodeType) => (
              <Button
                key={nodeType.id}
                variant="outline"
                className="w-full justify-start"
                onClick={() => addNode(nodeType)}
              >
                <div className={`w-3 h-3 rounded-full ${nodeType.color} mr-2`}></div>
                {nodeType.name}
              </Button>
            ))}
          </div>

          <div className="mt-8">
            <h2 className="font-semibold mb-4">Workflow Details</h2>
            <div className="text-sm space-y-2">
              <div className="flex justify-between">
                <span>Nodes:</span>
                <span>{nodes.length}</span>
              </div>
              <div className="flex justify-between">
                <span>Connections:</span>
                <span>{connections.length}</span>
              </div>
              <div className="flex justify-between">
                <span>Status:</span>
                <span className="text-green-600">Draft</span>
              </div>
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 relative bg-gray-50 overflow-auto">
          <div 
            ref={canvasRef}
            className="w-full h-full relative min-h-screen min-w-screen"
            style={{ 
              backgroundImage: 'radial-gradient(circle, #e5e7eb 1px, transparent 1px)',
              backgroundSize: '20px 20px'
            }}
          >
            {/* Render nodes */}
            {nodes.map((node) => (
              <div
                key={node.id}
                className={`absolute rounded-lg shadow-md border-2 p-3 cursor-move ${
                  selectedNode?.id === node.id ? 'border-blue-500' : 'border-gray-300'
                }`}
                style={{ left: node.position.x, top: node.position.y }}
                onClick={() => setSelectedNode(node)}
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full ${node.color} mr-2`}></div>
                    <span className="font-medium">{node.name}</span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 w-6 p-0"
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteNode(node.id);
                    }}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
                {selectedNode?.id === node.id && (
                  <div className="mt-2 p-2 bg-gray-100 rounded text-xs">
                    Node ID: {node.id}
                  </div>
                )}
              </div>
            ))}

            {/* Render connections */}
            {connections.map((conn, index) => (
              <svg
                key={index}
                className="absolute top-0 left-0 w-full h-full pointer-events-none"
                style={{ zIndex: 0 }}
              >
                <line
                  x1={150}
                  y1={150}
                  x2={300}
                  y2={300}
                  stroke="#6b7280"
                  strokeWidth="2"
                  markerEnd="url(#arrowhead)"
                />
                <defs>
                  <marker
                    id="arrowhead"
                    markerWidth="10"
                    markerHeight="7"
                    refX="9"
                    refY="3.5"
                    orient="auto"
                  >
                    <polygon
                      points="0 0, 10 3.5, 0 7"
                      fill="#6b7280"
                    />
                  </marker>
                </defs>
              </svg>
            ))}
          </div>
        </div>

        {/* Properties Panel */}
        {selectedNode && (
          <div className="w-80 border-l p-4 bg-white">
            <div className="flex justify-between items-center mb-4">
              <h2 className="font-semibold">Node Properties</h2>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedNode(null)}
              >
                Close
              </Button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Node Name</label>
                <input
                  type="text"
                  className="w-full border rounded px-2 py-1 text-sm"
                  value={selectedNode.data.label}
                  onChange={(e) => {
                    const updatedNodes = nodes.map(node =>
                      node.id === selectedNode.id
                        ? { ...node, data: { ...node.data, label: e.target.value } }
                        : node
                    );
                    setNodes(updatedNodes);
                    setSelectedNode({ ...selectedNode, data: { ...selectedNode.data, label: e.target.value } });
                  }}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  className="w-full border rounded px-2 py-1 text-sm h-24"
                  placeholder="Enter node description..."
                />
              </div>
              <div>
                <Button variant="outline" className="w-full" onClick={() => deleteNode(selectedNode.id)}>
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete Node
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkflowBuilder;
'''
    
    workflow_path = frontend_dir / "src" / "pages" / "WorkflowBuilder.jsx"
    with open(workflow_path, "w") as f:
        f.write(workflow_page)
    
    print("🔄 src/pages/WorkflowBuilder.jsx created")

def main():
    create_additional_components()
    print("\n✅ Additional frontend components created successfully!")

if __name__ == "__main__":
    main()