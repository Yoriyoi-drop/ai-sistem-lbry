import React from 'react';
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
  Search,
  Shield,
  AlertTriangle,
  Target,
  Clock,
  Eye,
  Ban,
  Check
} from 'lucide-react';

const Threats = () => {
  const threats = [
    {
      id: 1,
      type: 'SQL Injection',
      severity: 'critical',
      title: 'Potential SQL Injection in Login Form',
      description: 'Detected potential SQL injection vulnerability in user authentication endpoint',
      source: '192.168.1.100',
      detectedAt: '2024-01-15T10:30:00Z',
      status: 'active',
      confidence: 95
    },
    {
      id: 2,
      type: 'XSS Attack',
      severity: 'high',
      title: 'Reflected XSS in Search Parameter',
      description: 'Cross-site scripting vulnerability detected in search functionality',
      source: '203.0.113.45',
      detectedAt: '2024-01-15T09:45:00Z',
      status: 'investigating',
      confidence: 87
    },
    {
      id: 3,
      type: 'Brute Force',
      severity: 'medium',
      title: 'Multiple Failed Login Attempts',
      description: 'Unusual pattern of failed login attempts detected',
      source: '198.51.100.23',
      detectedAt: '2024-01-15T08:20:00Z',
      status: 'mitigated',
      confidence: 78
    },
    {
      id: 4,
      type: 'DDoS Attack',
      severity: 'critical',
      title: 'High Traffic Volume Detected',
      description: 'Unusual traffic spike detected on web application',
      source: 'Multiple IPs',
      detectedAt: '2024-01-15T07:15:00Z',
      status: 'active',
      confidence: 92
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'high': return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
      case 'medium': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'low': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'investigating': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'mitigated': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'false_positive': return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Threat Intelligence</h1>
          <p className="text-gray-400 mt-1">Monitor and manage detected security threats</p>
        </div>
        <div className="flex gap-3">
          <Button className="bg-red-600 hover:bg-red-700">
            <Shield className="w-4 h-4 mr-2" />
            New Threat Intel
          </Button>
          <Button variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700">
            <Search className="w-4 h-4 mr-2" />
            Filter
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Threats</p>
                <p className="text-2xl font-bold">{threats.filter(t => t.status === 'active').length}</p>
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
                <p className="text-gray-400 text-sm">Critical</p>
                <p className="text-2xl font-bold">{threats.filter(t => t.severity === 'critical').length}</p>
              </div>
              <div className="bg-red-500/20 p-3 rounded-lg">
                <Shield className="w-6 h-6 text-red-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">High Risk</p>
                <p className="text-2xl font-bold">{threats.filter(t => t.severity === 'high').length}</p>
              </div>
              <div className="bg-orange-500/20 p-3 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-orange-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Mitigated</p>
                <p className="text-2xl font-bold">{threats.filter(t => t.status === 'mitigated').length}</p>
              </div>
              <div className="bg-green-500/20 p-3 rounded-lg">
                <Check className="w-6 h-6 text-green-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Threats Table */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle>Detected Threats</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-700">
                <TableHead className="text-gray-300">Type</TableHead>
                <TableHead className="text-gray-300">Title</TableHead>
                <TableHead className="text-gray-300">Severity</TableHead>
                <TableHead className="text-gray-300">Status</TableHead>
                <TableHead className="text-gray-300">Source</TableHead>
                <TableHead className="text-gray-300">Detected</TableHead>
                <TableHead className="text-gray-300">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {threats.map((threat) => (
                <TableRow key={threat.id} className="border-gray-700 hover:bg-gray-750">
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className={`w-4 h-4 ${threat.severity === 'critical' ? 'text-red-500' : threat.severity === 'high' ? 'text-orange-500' : threat.severity === 'medium' ? 'text-yellow-500' : 'text-blue-500'}`} />
                      {threat.type}
                    </div>
                  </TableCell>
                  <TableCell className="text-gray-300">{threat.title}</TableCell>
                  <TableCell>
                    <Badge className={getSeverityColor(threat.severity)}>
                      {threat.severity}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(threat.status)}>
                      {threat.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-gray-300">{threat.source}</TableCell>
                  <TableCell className="text-gray-300">{formatDate(threat.detectedAt)}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
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
                        className="border-green-500 text-green-400 hover:bg-green-500/20"
                      >
                        <Check className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="border-red-500 text-red-400 hover:bg-red-500/20"
                      >
                        <Ban className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle>Recent Threat Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 bg-gray-700 rounded-lg">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium">SQL Injection blocked</h3>
                  <p className="text-sm text-gray-400 mt-1">Potential SQL injection from 192.168.1.100 blocked</p>
                </div>
                <div className="text-sm text-gray-400">2 minutes ago</div>
              </div>
              <div className="mt-2 flex gap-2">
                <Badge variant="destructive">Critical</Badge>
                <Badge variant="outline" className="border-gray-600 text-gray-300">Blocked</Badge>
              </div>
            </div>
            
            <div className="p-4 bg-gray-700 rounded-lg">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium">XSS Attack detected</h3>
                  <p className="text-sm text-gray-400 mt-1">Cross-site scripting attempt on search endpoint</p>
                </div>
                <div className="text-sm text-gray-400">5 minutes ago</div>
              </div>
              <div className="mt-2 flex gap-2">
                <Badge variant="default">High</Badge>
                <Badge variant="outline" className="border-yellow-600 text-yellow-400">Investigating</Badge>
              </div>
            </div>
            
            <div className="p-4 bg-gray-700 rounded-lg">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium">Brute force mitigation</h3>
                  <p className="text-sm text-gray-400 mt-1">Successfully mitigated login brute force attack</p>
                </div>
                <div className="text-sm text-gray-400">10 minutes ago</div>
              </div>
              <div className="mt-2 flex gap-2">
                <Badge variant="outline" className="border-green-600 text-green-400">Mitigated</Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Threats;