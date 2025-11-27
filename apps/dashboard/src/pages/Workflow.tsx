import React, { useState } from 'react';
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
  Input
} from '../components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '../components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '../components/ui/dialog';
import {
  Play,
  Pause,
  RotateCcw,
  Download,
  Eye,
  Plus,
  Workflow,
  Activity,
  Clock,
  CheckCircle,
  XCircle
} from 'lucide-react';

const Workflow = () => {
  const [workflows, setWorkflows] = useState([
    {
      id: 1,
      name: 'Security Scanning Workflow',
      description: 'Automated security scanning and reporting pipeline',
      status: 'running',
      createdAt: '2024-01-15T10:30:00Z',
      lastRun: '2024-01-15T12:45:00Z',
      runs: 24,
      successRate: 98.5
    },
    {
      id: 2,
      name: 'Threat Response Workflow',
      description: 'Automated threat detection and response pipeline',
      status: 'completed',
      createdAt: '2024-01-14T09:15:00Z',
      lastRun: '2024-01-15T11:30:00Z',
      runs: 42,
      successRate: 96.2
    },
    {
      id: 3,
      name: 'Compliance Checking',
      description: 'Periodic compliance and audit workflow',
      status: 'pending',
      createdAt: '2024-01-13T14:20:00Z',
      lastRun: '2024-01-14T16:45:00Z',
      runs: 15,
      successRate: 100
    },
    {
      id: 4,
      name: 'Agent Deployment',
      description: 'Automated AI security agent deployment workflow',
      status: 'failed',
      createdAt: '2024-01-12T08:30:00Z',
      lastRun: '2024-01-12T09:15:00Z',
      runs: 3,
      successRate: 66.7
    }
  ]);

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newWorkflow, setNewWorkflow] = useState({
    name: '',
    description: '',
    trigger: 'manual'
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'completed': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'pending': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'failed': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const handleRunWorkflow = (workflowId: number) => {
    setWorkflows(prev => prev.map(workflow =>
      workflow.id === workflowId
        ? { ...workflow, status: 'running', lastRun: new Date().toISOString(), runs: workflow.runs + 1 }
        : workflow
    ));
  };

  const handleCreateWorkflow = () => {
    const newWorkflowObj = {
      id: workflows.length + 1,
      name: newWorkflow.name,
      description: newWorkflow.description,
      status: 'pending',
      createdAt: new Date().toISOString(),
      lastRun: null,
      runs: 0,
      successRate: 0
    };

    setWorkflows([newWorkflowObj, ...workflows]);
    setIsDialogOpen(false);
    setNewWorkflow({ name: '', description: '', trigger: 'manual' });
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Workflow Automation</h1>
          <p className="text-gray-400 mt-1">Manage and monitor security automation workflows</p>
        </div>
        <div className="flex gap-3">
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-blue-600 hover:bg-blue-700">
                <Plus className="w-4 h-4 mr-2" />
                New Workflow
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md bg-gray-800 border-gray-700">
              <DialogHeader>
                <DialogTitle>Create New Workflow</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div>
                  <label className="text-sm font-medium text-gray-300">Workflow Name</label>
                  <Input
                    value={newWorkflow.name}
                    onChange={(e) => setNewWorkflow(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Enter workflow name"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Description</label>
                  <Input
                    value={newWorkflow.description}
                    onChange={(e) => setNewWorkflow(prev => ({ ...prev, description: e.target.value }))}
                    placeholder="Enter workflow description"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Trigger</label>
                  <Select value={newWorkflow.trigger} onValueChange={(value) => setNewWorkflow(prev => ({ ...prev, trigger: value }))}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      <SelectItem value="manual">Manual</SelectItem>
                      <SelectItem value="scheduled">Scheduled</SelectItem>
                      <SelectItem value="event">Event-based</SelectItem>
                      <SelectItem value="webhook">Webhook</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="flex gap-3 pt-4">
                <Button
                  onClick={handleCreateWorkflow}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  Create Workflow
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
            Export Workflows
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Workflows</p>
                <p className="text-2xl font-bold">{workflows.length}</p>
              </div>
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Workflow className="w-6 h-6 text-blue-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Workflows</p>
                <p className="text-2xl font-bold">{workflows.filter(w => w.status === 'running' || w.status === 'pending').length}</p>
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
                <p className="text-gray-400 text-sm">Total Runs</p>
                <p className="text-2xl font-bold">{workflows.reduce((sum, workflow) => sum + workflow.runs, 0)}</p>
              </div>
              <div className="bg-purple-500/20 p-3 rounded-lg">
                <Activity className="w-6 h-6 text-purple-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Avg Success Rate</p>
                <p className="text-2xl font-bold">
                  {workflows.length > 0
                    ? Math.round(workflows.reduce((sum, workflow) => sum + workflow.successRate, 0) / workflows.length) + '%'
                    : '0%'}
                </p>
              </div>
              <div className="bg-yellow-500/20 p-3 rounded-lg">
                <CheckCircle className="w-6 h-6 text-yellow-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Workflows Table */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle>Workflow Management</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-700">
                <TableHead className="text-gray-300">Name</TableHead>
                <TableHead className="text-gray-300">Description</TableHead>
                <TableHead className="text-gray-300">Status</TableHead>
                <TableHead className="text-gray-300">Runs</TableHead>
                <TableHead className="text-gray-300">Success Rate</TableHead>
                <TableHead className="text-gray-300">Last Run</TableHead>
                <TableHead className="text-gray-300">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {workflows.map((workflow) => (
                <TableRow key={workflow.id} className="border-gray-700 hover:bg-gray-750">
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-3">
                      <Workflow className="w-4 h-4 text-blue-400" />
                      <div>
                        {workflow.name}
                        {workflow.status === 'running' && (
                          <div className="w-2 h-2 bg-green-500 rounded-full ml-2 inline-block animate-pulse"></div>
                        )}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="text-gray-300">{workflow.description}</TableCell>
                  <TableCell>
                    <Badge className={`border ${getStatusColor(workflow.status)}`}>
                      <div className="w-2 h-2 rounded-full mr-2 inline-block bg-current"></div>
                      {workflow.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-gray-300">{workflow.runs}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="w-16 bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            workflow.successRate > 90 ? 'bg-green-500' :
                            workflow.successRate > 70 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${workflow.successRate}%` }}
                        ></div>
                      </div>
                      <span>{workflow.successRate}%</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-gray-300">{formatDate(workflow.lastRun)}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      {workflow.status !== 'running' && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleRunWorkflow(workflow.id)}
                          className="border-green-500 text-green-400 hover:bg-green-500/20"
                        >
                          <Play className="w-4 h-4" />
                        </Button>
                      )}
                      {workflow.status === 'running' && (
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-red-500 text-red-400 hover:bg-red-500/20"
                        >
                          <Pause className="w-4 h-4" />
                        </Button>
                      )}
                      <Button
                        size="sm"
                        variant="outline"
                        className="border-blue-500 text-blue-400 hover:bg-blue-500/20"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="border-gray-600 text-gray-300 hover:bg-gray-700"
                      >
                        <RotateCcw className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Workflow Details Panel */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle>Workflow Configuration</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium mb-3">Recent Activity</h3>
              <div className="space-y-3">
                <div className="p-3 bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-4 h-4 text-green-400" />
                    </div>
                    <div>
                      <p className="font-medium">Security Scanning completed</p>
                      <p className="text-sm text-gray-400">Workflow completed successfully</p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">2 minutes ago</p>
                </div>
                <div className="p-3 bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
                      <Activity className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <p className="font-medium">Threat Response started</p>
                      <p className="text-sm text-gray-400">Workflow initiated automatically</p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">5 minutes ago</p>
                </div>
                <div className="p-3 bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center">
                      <XCircle className="w-4 h-4 text-red-400" />
                    </div>
                    <div>
                      <p className="font-medium">Agent Deployment failed</p>
                      <p className="text-sm text-gray-400">Error during deployment process</p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">10 minutes ago</p>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-3">Workflow Templates</h3>
              <div className="space-y-3">
                <div className="p-3 bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-650 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                      <Workflow className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <p className="font-medium">Security Scanning Template</p>
                      <p className="text-sm text-gray-400">Automated vulnerability scanning</p>
                    </div>
                  </div>
                </div>
                <div className="p-3 bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-650 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                      <Activity className="w-4 h-4 text-green-400" />
                    </div>
                    <div>
                      <p className="font-medium">Threat Response Template</p>
                      <p className="text-sm text-gray-400">Automated threat mitigation</p>
                    </div>
                  </div>
                </div>
                <div className="p-3 bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-650 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center">
                      <CheckCircle className="w-4 h-4 text-purple-400" />
                    </div>
                    <div>
                      <p className="font-medium">Compliance Template</p>
                      <p className="text-sm text-gray-400">Periodic compliance checks</p>
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

export default Workflow;