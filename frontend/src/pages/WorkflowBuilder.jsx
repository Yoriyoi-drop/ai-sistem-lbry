import React, { useState, useRef } from 'react';
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
