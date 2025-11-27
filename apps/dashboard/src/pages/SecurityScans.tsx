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
  Tabs, 
  TabsContent, 
  TabsList, 
  TabsTrigger 
} from '../components/ui/tabs';
import {
  Search,
  Play,
  Pause,
  RotateCcw,
  Download,
  Eye,
  AlertTriangle,
  Shield,
  Target,
  Clock,
  CheckCircle,
  XCircle
} from 'lucide-react';

const SecurityScans = () => {
  const [scans, setScans] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const [newScan, setNewScan] = useState({
    name: '',
    target: '',
    type: 'vulnerability',
    schedule: 'manual'
  });

  useEffect(() => {
    // Mock data for scans
    setScans([
      {
        id: 1,
        name: 'Network Infrastructure Scan',
        target: '10.0.0.0/24',
        type: 'vulnerability',
        status: 'completed',
        severity: 'high',
        startTime: '2024-01-15T10:30:00Z',
        endTime: '2024-01-15T11:45:00Z',
        threatsFound: 12,
        vulnerabilities: 5,
        critical: 2,
        high: 3,
        medium: 0,
        low: 0
      },
      {
        id: 2,
        name: 'Web Application Scan',
        target: 'https://example.com',
        type: 'web',
        status: 'running',
        severity: 'medium',
        startTime: '2024-01-15T12:00:00Z',
        endTime: null,
        threatsFound: 3,
        vulnerabilities: 8,
        critical: 0,
        high: 1,
        medium: 2,
        low: 5
      },
      {
        id: 3,
        name: 'Compliance Scan',
        target: 'PCI-DSS Requirements',
        type: 'compliance',
        status: 'pending',
        severity: 'medium',
        startTime: null,
        endTime: null,
        threatsFound: 0,
        vulnerabilities: 0,
        critical: 0,
        high: 0,
        medium: 0,
        low: 0
      },
      {
        id: 4,
        name: 'API Security Scan',
        target: 'https://api.example.com',
        type: 'api',
        status: 'failed',
        severity: 'critical',
        startTime: '2024-01-14T14:20:00Z',
        endTime: '2024-01-14T14:25:00Z',
        threatsFound: 0,
        vulnerabilities: 0,
        critical: 0,
        high: 0,
        medium: 0,
        low: 0
      }
    ]);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'running': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'pending': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'failed': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'vulnerability': return 'text-purple-400';
      case 'web': return 'text-blue-400';
      case 'compliance': return 'text-yellow-400';
      case 'api': return 'text-green-400';
      default: return 'text-gray-400';
    }
  };

  const handleStartScan = (scanId) => {
    setScans(prev => prev.map(scan => 
      scan.id === scanId ? { ...scan, status: 'running', startTime: new Date().toISOString() } : scan
    ));
  };

  const handleStopScan = (scanId) => {
    setScans(prev => prev.map(scan => 
      scan.id === scanId ? { ...scan, status: 'completed', endTime: new Date().toISOString() } : scan
    ));
  };

  const handleCreateScan = () => {
    const newScanObj = {
      id: scans.length + 1,
      ...newScan,
      status: 'pending',
      severity: 'medium',
      startTime: null,
      endTime: null,
      threatsFound: 0,
      vulnerabilities: 0,
      critical: 0,
      high: 0,
      medium: 0,
      low: 0
    };
    
    setScans([newScanObj, ...scans]);
    setIsDialogOpen(false);
    setNewScan({ name: '', target: '', type: 'vulnerability', schedule: 'manual' });
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'high': return <AlertTriangle className="w-4 h-4 text-orange-500" />;
      case 'medium': return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      case 'low': return <Shield className="w-4 h-4 text-blue-500" />;
      default: return <Shield className="w-4 h-4 text-gray-500" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Security Scans</h1>
          <p className="text-gray-400 mt-1">Monitor and manage security scanning operations</p>
        </div>
        <div className="flex gap-3">
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-blue-600 hover:bg-blue-700">
                <Shield className="w-4 h-4 mr-2" />
                New Scan
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md bg-gray-800 border-gray-700">
              <DialogHeader>
                <DialogTitle>Create New Scan</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div>
                  <label className="text-sm font-medium text-gray-300">Scan Name</label>
                  <Input
                    value={newScan.name}
                    onChange={(e) => setNewScan(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Enter scan name"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Target</label>
                  <Input
                    value={newScan.target}
                    onChange={(e) => setNewScan(prev => ({ ...prev, target: e.target.value }))}
                    placeholder="Enter target (URL, IP, etc.)"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Scan Type</label>
                  <Select value={newScan.type} onValueChange={(value) => setNewScan(prev => ({ ...prev, type: value }))}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      <SelectItem value="vulnerability">Vulnerability Scan</SelectItem>
                      <SelectItem value="web">Web Application Scan</SelectItem>
                      <SelectItem value="compliance">Compliance Scan</SelectItem>
                      <SelectItem value="api">API Security Scan</SelectItem>
                      <SelectItem value="network">Network Scan</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Schedule</label>
                  <Select value={newScan.schedule} onValueChange={(value) => setNewScan(prev => ({ ...prev, schedule: value }))}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      <SelectItem value="manual">Manual</SelectItem>
                      <SelectItem value="daily">Daily</SelectItem>
                      <SelectItem value="weekly">Weekly</SelectItem>
                      <SelectItem value="monthly">Monthly</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="flex gap-3 pt-4">
                <Button 
                  onClick={handleCreateScan}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  Create Scan
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
            Export Reports
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Scans</p>
                <p className="text-2xl font-bold">{scans.length}</p>
              </div>
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Shield className="w-6 h-6 text-blue-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Scans</p>
                <p className="text-2xl font-bold">{scans.filter(s => s.status === 'running').length}</p>
              </div>
              <div className="bg-green-500/20 p-3 rounded-lg">
                <Play className="w-6 h-6 text-green-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Threats Found</p>
                <p className="text-2xl font-bold">{scans.reduce((sum, scan) => sum + (scan.threatsFound || 0), 0)}</p>
              </div>
              <div className="bg-red-500/20 p-3 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-red-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Vulnerabilities</p>
                <p className="text-2xl font-bold">{scans.reduce((sum, scan) => sum + (scan.vulnerabilities || 0), 0)}</p>
              </div>
              <div className="bg-yellow-500/20 p-3 rounded-lg">
                <Target className="w-6 h-6 text-yellow-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Scans Table */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle>Scan Results</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-700">
                <TableHead className="text-gray-300">Name</TableHead>
                <TableHead className="text-gray-300">Target</TableHead>
                <TableHead className="text-gray-300">Type</TableHead>
                <TableHead className="text-gray-300">Status</TableHead>
                <TableHead className="text-gray-300">Threats</TableHead>
                <TableHead className="text-gray-300">Started</TableHead>
                <TableHead className="text-gray-300">Duration</TableHead>
                <TableHead className="text-gray-300">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {scans.map((scan) => (
                <TableRow key={scan.id} className="border-gray-700 hover:bg-gray-750">
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      {getSeverityIcon(scan.severity)}
                      {scan.name}
                    </div>
                  </TableCell>
                  <TableCell className="text-gray-300">{scan.target}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className={`${getTypeColor(scan.type)} border-gray-600`}>
                      {scan.type}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={`border ${getStatusColor(scan.status)}`}>
                      {scan.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <AlertTriangle className="w-4 h-4 text-red-500" />
                      <span>{scan.threatsFound}</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-gray-300">{formatDate(scan.startTime)}</TableCell>
                  <TableCell className="text-gray-300">
                    {scan.startTime && scan.endTime ? 
                      `${Math.round((new Date(scan.endTime) - new Date(scan.startTime)) / 60000)}m` : 
                      '-'
                    }
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      {scan.status === 'pending' && (
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleStartScan(scan.id)}
                          className="border-green-500 text-green-400 hover:bg-green-500/20"
                        >
                          <Play className="w-4 h-4" />
                        </Button>
                      )}
                      {scan.status === 'running' && (
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleStopScan(scan.id)}
                          className="border-red-500 text-red-400 hover:bg-red-500/20"
                        >
                          <Pause className="w-4 h-4" />
                        </Button>
                      )}
                      {scan.status === 'completed' && (
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => {
                            setSelectedScan(scan);
                            setIsDialogOpen(true);
                          }}
                          className="border-blue-500 text-blue-400 hover:bg-blue-500/20"
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                      )}
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

      {/* Scan Details Dialog */}
      {selectedScan && (
        <Dialog open={!!selectedScan} onOpenChange={() => setSelectedScan(null)}>
          <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto bg-gray-800 border-gray-700">
            <DialogHeader>
              <DialogTitle>Scan Details: {selectedScan.name}</DialogTitle>
            </DialogHeader>
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h3 className="text-sm font-medium text-gray-400">Target</h3>
                  <p className="text-white">{selectedScan.target}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-400">Type</h3>
                  <p className="text-white capitalize">{selectedScan.type}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-400">Status</h3>
                  <Badge className={getStatusColor(selectedScan.status)}>
                    {selectedScan.status}
                  </Badge>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-400">Started</h3>
                  <p className="text-white">{formatDate(selectedScan.startTime)}</p>
                </div>
              </div>
              
              <div className="grid grid-cols-4 gap-4">
                <div className="text-center p-4 bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-red-400">{selectedScan.critical || 0}</div>
                  <div className="text-gray-400 text-sm">Critical</div>
                </div>
                <div className="text-center p-4 bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-orange-400">{selectedScan.high || 0}</div>
                  <div className="text-gray-400 text-sm">High</div>
                </div>
                <div className="text-center p-4 bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-yellow-400">{selectedScan.medium || 0}</div>
                  <div className="text-gray-400 text-sm">Medium</div>
                </div>
                <div className="text-center p-4 bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-blue-400">{selectedScan.low || 0}</div>
                  <div className="text-gray-400 text-sm">Low</div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-medium mb-3">Scan Results</h3>
                <Tabs defaultValue="vulnerabilities">
                  <TabsList className="grid w-full grid-cols-3 bg-gray-700">
                    <TabsTrigger value="vulnerabilities" className="text-gray-300 data-[state=active]:bg-gray-600">Vulnerabilities</TabsTrigger>
                    <TabsTrigger value="threats" className="text-gray-300 data-[state=active]:bg-gray-600">Threats</TabsTrigger>
                    <TabsTrigger value="logs" className="text-gray-300 data-[state=active]:bg-gray-600">Logs</TabsTrigger>
                  </TabsList>
                  <TabsContent value="vulnerabilities" className="mt-4">
                    <div className="space-y-3">
                      <div className="p-3 bg-gray-700 rounded-lg">
                        <div className="flex justify-between items-center">
                          <span className="font-medium">SQL Injection Vulnerability</span>
                          <Badge variant="destructive">Critical</Badge>
                        </div>
                        <p className="text-sm text-gray-400 mt-1">Potential SQL injection in login form parameter</p>
                      </div>
                      <div className="p-3 bg-gray-700 rounded-lg">
                        <div className="flex justify-between items-center">
                          <span className="font-medium">Cross-Site Scripting</span>
                          <Badge variant="default">High</Badge>
                        </div>
                        <p className="text-sm text-gray-400 mt-1">Reflected XSS in search parameter</p>
                      </div>
                    </div>
                  </TabsContent>
                  <TabsContent value="threats" className="mt-4">
                    <p className="text-gray-400">No additional threat details available.</p>
                  </TabsContent>
                  <TabsContent value="logs" className="mt-4">
                    <div className="bg-gray-900 p-4 rounded-lg max-h-60 overflow-y-auto font-mono text-sm">
                      <div className="text-green-400">[INFO] Scan started at {formatDate(selectedScan.startTime)}</div>
                      <div className="text-yellow-400">[WARN] Potential vulnerability detected at path /login</div>
                      <div className="text-red-400">[ERROR] SQL injection vulnerability confirmed</div>
                      <div className="text-green-400">[INFO] Scan completed successfully</div>
                    </div>
                  </TabsContent>
                </Tabs>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
};

export default SecurityScans;