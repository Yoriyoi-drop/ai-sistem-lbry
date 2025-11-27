import React, { useState, useEffect } from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle 
} from '../components/ui/card';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '../components/ui/table';
import { 
  Badge 
} from '../components/ui/badge';
import { 
  Button 
} from '../components/ui/button';
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle,
  DialogTrigger 
} from '../components/ui/dialog';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue 
} from '../components/ui/select';
import { 
  Input 
} from '../components/ui/input';
import {
  Plus,
  Play,
  Pause,
  RotateCcw,
  Download,
  Eye,
  AlertTriangle,
  Shield,
  Bot,
  Activity,
  Clock,
  Check,
  X,
  Settings
} from 'lucide-react';

const Agents = () => {
  const [agents, setAgents] = useState([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    type: 'security_scanner',
    description: ''
  });

  useEffect(() => {
    // Mock data for agents
    setAgents([
      {
        id: 1,
        name: 'Network Scanner',
        description: 'Scans network for open ports and services',
        status: 'active',
        agentType: 'security_scanner',
        lastHeartbeat: '2024-01-15T10:30:00Z',
        tasksCompleted: 142,
        efficiency: 98.5,
        memoryUsage: 45,
        cpuUsage: 12,
        isActive: true
      },
      {
        id: 2,
        name: 'Web Vulnerability Scanner',
        description: 'Scans web applications for vulnerabilities',
        status: 'active',
        agentType: 'vulnerability_scanner',
        lastHeartbeat: '2024-01-15T10:29:45Z',
        tasksCompleted: 89,
        efficiency: 96.2,
        memoryUsage: 67,
        cpuUsage: 18,
        isActive: true
      },
      {
        id: 3,
        name: 'Threat Analyzer',
        description: 'Analyzes detected threats and provides recommendations',
        status: 'inactive',
        agentType: 'threat_analyzer',
        lastHeartbeat: '2024-01-15T09:45:22Z',
        tasksCompleted: 234,
        efficiency: 99.1,
        memoryUsage: 32,
        cpuUsage: 8,
        isActive: false
      },
      {
        id: 4,
        name: 'Compliance Checker',
        description: 'Checks for compliance with security standards',
        status: 'error',
        agentType: 'compliance_checker',
        lastHeartbeat: '2024-01-15T08:15:30Z',
        tasksCompleted: 56,
        efficiency: 87.3,
        memoryUsage: 78,
        cpuUsage: 25,
        isActive: false
      }
    ]);
  }, []);

  const getAgentTypeIcon = (type) => {
    switch (type) {
      case 'security_scanner': return <Shield className="w-4 h-4 text-blue-400" />;
      case 'vulnerability_scanner': return <AlertTriangle className="w-4 h-4 text-red-400" />;
      case 'threat_analyzer': return <Eye className="w-4 h-4 text-purple-400" />;
      case 'compliance_checker': return <CheckCircle className="w-4 h-4 text-green-400" />;
      default: return <Bot className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'inactive': return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
      case 'error': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'warning': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const handleToggleAgent = (agentId) => {
    setAgents(prev => prev.map(agent => 
      agent.id === agentId 
        ? { 
            ...agent, 
            isActive: !agent.isActive,
            status: !agent.isActive ? 'active' : 'inactive'
          } 
        : agent
    ));
  };

  const handleCreateAgent = () => {
    const newAgentObj = {
      id: agents.length + 1,
      ...newAgent,
      status: 'inactive',
      lastHeartbeat: new Date().toISOString(),
      tasksCompleted: 0,
      efficiency: 0,
      memoryUsage: 0,
      cpuUsage: 0,
      isActive: false
    };
    
    setAgents([newAgentObj, ...agents]);
    setIsDialogOpen(false);
    setNewAgent({ name: '', type: 'security_scanner', description: '' });
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-bold">Security Agents</h1>
          <p className="text-gray-400 mt-1">Manage and monitor AI security agents</p>
        </div>
        <div className="flex gap-3">
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Add Agent
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md bg-gray-800 border-gray-700">
              <DialogHeader>
                <DialogTitle>Add New Agent</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div>
                  <label className="text-sm font-medium text-gray-300">Agent Name</label>
                  <Input
                    value={newAgent.name}
                    onChange={(e) => setNewAgent(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Enter agent name"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Agent Type</label>
                  <Select value={newAgent.type} onValueChange={(value) => setNewAgent(prev => ({ ...prev, type: value }))}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      <SelectItem value="security_scanner">Security Scanner</SelectItem>
                      <SelectItem value="vulnerability_scanner">Vulnerability Scanner</SelectItem>
                      <SelectItem value="threat_analyzer">Threat Analyzer</SelectItem>
                      <SelectItem value="compliance_checker">Compliance Checker</SelectItem>
                      <SelectItem value="honeypot">Honeypot Agent</SelectItem>
                      <SelectItem value="behavioral_analyzer">Behavioral Analyzer</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Description</label>
                  <Input
                    value={newAgent.description}
                    onChange={(e) => setNewAgent(prev => ({ ...prev, description: e.target.value }))}
                    placeholder="Enter agent description"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>
              </div>
              <div className="flex gap-3 pt-4">
                <Button 
                  onClick={handleCreateAgent}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  Create Agent
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => setIsDialogOpen(false)}
                  className="flex-1 border-gray-600 text-gray-300 hover:bg-gray-700"
                >
                  Cancel
                </Button>
              </div>
            </DialogContent>
          </Dialog>
          <Button variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700">
            <Download className="w-4 h-4 mr-2" />
            Export Agents
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Agents</p>
                <p className="text-2xl font-bold">{agents.length}</p>
              </div>
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Bot className="w-6 h-6 text-blue-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Agents</p>
                <p className="text-2xl font-bold">{agents.filter(a => a.status === 'active').length}</p>
              </div>
              <div className="bg-green-500/20 p-3 rounded-lg">
                <Activity className="w-6 h-6 text-green-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Tasks Completed</p>
                <p className="text-2xl font-bold">
                  {agents.reduce((sum, agent) => sum + agent.tasksCompleted, 0)}
                </p>
              </div>
              <div className="bg-purple-500/20 p-3 rounded-lg">
                <Check className="w-6 h-6 text-purple-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Avg Efficiency</p>
                <p className="text-2xl font-bold">
                  {agents.length > 0 
                    ? Math.round(agents.reduce((sum, agent) => sum + agent.efficiency, 0) / agents.length) + '%' 
                    : '0%'}
                </p>
              </div>
              <div className="bg-yellow-500/20 p-3 rounded-lg">
                <Shield className="w-6 h-6 text-yellow-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Agents Table */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle>Agent Management</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-700">
                <TableHead className="text-gray-300">Name</TableHead>
                <TableHead className="text-gray-300">Type</TableHead>
                <TableHead className="text-gray-300">Status</TableHead>
                <TableHead className="text-gray-300">Efficiency</TableHead>
                <TableHead className="text-gray-300">Tasks</TableHead>
                <TableHead className="text-gray-300">Last Heartbeat</TableHead>
                <TableHead className="text-gray-300">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {agents.map((agent) => (
                <TableRow key={agent.id} className="border-gray-700 hover:bg-gray-750">
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-3">
                      {getAgentTypeIcon(agent.agentType)}
                      <div>
                        <div className="flex items-center gap-2">
                          {agent.name}
                          {agent.isActive && (
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                          )}
                        </div>
                        <p className="text-gray-400 text-sm">{agent.description}</p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="capitalize border-gray-600 text-gray-300">
                      {agent.agentType.replace('_', ' ')}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={`border ${getStatusColor(agent.status)}`}>
                      <div className="w-2 h-2 rounded-full mr-2 inline-block bg-current"></div>
                      {agent.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="w-16 bg-gray-700 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            agent.efficiency > 90 ? 'bg-green-500' : 
                            agent.efficiency > 70 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${agent.efficiency}%` }}
                        ></div>
                      </div>
                      <span>{agent.efficiency}%</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-gray-300">{agent.tasksCompleted}</TableCell>
                  <TableCell className="text-gray-300">{formatDate(agent.lastHeartbeat)}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      {agent.isActive ? (
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleToggleAgent(agent.id)}
                          className="border-red-500 text-red-400 hover:bg-red-500/20"
                        >
                          <Pause className="w-4 h-4" />
                        </Button>
                      ) : (
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleToggleAgent(agent.id)}
                          className="border-green-500 text-green-400 hover:bg-green-500/20"
                        >
                          <Play className="w-4 h-4" />
                        </Button>
                      )}
                      <Button 
                        size="sm" 
                        variant="outline" 
                        className="border-blue-500 text-blue-400 hover:bg-blue-500/20"
                      >
                        <Settings className="w-4 h-4" />
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline" 
                        className="border-gray-600 text-gray-300 hover:bg-gray-700"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Agent Details Panel */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle>Agent Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium mb-3">Resource Usage</h3>
              <div className="space-y-4">
                {agents.slice(0, 3).map((agent) => (
                  <div key={agent.id} className="p-3 bg-gray-700 rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium">{agent.name}</span>
                      <Badge variant="outline" className="border-gray-600 text-gray-300">
                        {agent.agentType.replace('_', ' ')}
                      </Badge>
                    </div>
                    <div className="space-y-2">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-400">CPU</span>
                          <span>{agent.cpuUsage}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="h-2 rounded-full bg-blue-500" 
                            style={{ width: `${agent.cpuUsage}%` }}
                          ></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-400">Memory</span>
                          <span>{agent.memoryUsage}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="h-2 rounded-full bg-green-500" 
                            style={{ width: `${agent.memoryUsage}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="font-medium mb-3">Recent Activity</h3>
              <div className="space-y-3">
                <div className="p-3 bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
                      <Check className="w-4 h-4 text-green-400" />
                    </div>
                    <div>
                      <p className="font-medium">Web Scanner completed scan</p>
                      <p className="text-sm text-gray-400">2 minutes ago</p>
                    </div>
                  </div>
                </div>
                <div className="p-3 bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center">
                      <Shield className="w-4 h-4 text-red-400" />
                    </div>
                    <div>
                      <p className="font-medium">Threat detected by Network Scanner</p>
                      <p className="text-sm text-gray-400">5 minutes ago</p>
                    </div>
                  </div>
                </div>
                <div className="p-3 bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
                      <Bot className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <p className="font-medium">Agent Heartbeat received</p>
                      <p className="text-sm text-gray-400">10 minutes ago</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Agents;