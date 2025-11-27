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
  Shield,
  AlertTriangle,
  Target,
  Clock,
  Eye,
  TrendingUp,
  Lock,
  Activity,
  BarChart3
} from 'lucide-react';

const Security = () => {
  const [stats, setStats] = useState({
    totalScans: 0,
    vulnerabilities: 0,
    threats: 0,
    securityScore: 0
  });

  const [recentScans, setRecentScans] = useState([]);
  const [vulnerabilities, setVulnerabilities] = useState([]);

  useEffect(() => {
    // Mock data initialization
    setStats({
      totalScans: 24,
      vulnerabilities: 12,
      threats: 5,
      securityScore: 87
    });

    setRecentScans([
      {
        id: 1,
        name: 'Website Security Scan',
        type: 'Web Application',
        status: 'completed',
        date: '2024-01-15T10:30:00Z',
        vulnerabilities: 3,
        threats: 1
      },
      {
        id: 2,
        name: 'Network Infrastructure Scan',
        type: 'Network',
        status: 'completed',
        date: '2024-01-15T09:45:00Z',
        vulnerabilities: 2,
        threats: 0
      },
      {
        id: 3,
        name: 'API Endpoint Scan',
        type: 'API Security',
        status: 'running',
        date: '2024-01-15T08:20:00Z',
        vulnerabilities: 0,
        threats: 0
      },
      {
        id: 4,
        name: 'Code Review Scan',
        type: 'Source Code',
        status: 'pending',
        date: '2024-01-15T07:15:00Z',
        vulnerabilities: 0,
        threats: 0
      }
    ]);

    setVulnerabilities([
      {
        id: 1,
        name: 'SQL Injection Vulnerability',
        severity: 'critical',
        status: 'open',
        discovered: '2024-01-14T10:30:00Z'
      },
      {
        id: 2,
        name: 'Cross-Site Scripting (XSS)',
        severity: 'high',
        status: 'in_progress',
        discovered: '2024-01-14T09:45:00Z'
      },
      {
        id: 3,
        name: 'Information Disclosure',
        severity: 'medium',
        status: 'resolved',
        discovered: '2024-01-13T15:20:00Z'
      },
      {
        id: 4,
        name: 'Weak Authentication',
        severity: 'high',
        status: 'open',
        discovered: '2024-01-12T11:30:00Z'
      }
    ]);
  }, []);

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
      case 'completed': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'running': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'pending': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'failed': return 'bg-red-500/20 text-red-400 border-red-500/30';
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
          <h1 className="text-3xl font-bold">Security Overview</h1>
          <p className="text-gray-400 mt-1">Monitor and manage your security posture</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Shield className="w-4 h-4 mr-2" />
          New Security Scan
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Security Score</p>
                <p className="text-2xl font-bold">{stats.securityScore}%</p>
              </div>
              <div className="bg-green-500/20 p-3 rounded-lg">
                <Shield className="w-6 h-6 text-green-400" />
              </div>
            </div>
            <div className="mt-2">
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="h-2 rounded-full bg-green-500"
                  style={{ width: `${stats.securityScore}%` }}
                ></div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Scans</p>
                <p className="text-2xl font-bold">{stats.totalScans}</p>
              </div>
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Activity className="w-6 h-6 text-blue-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Vulnerabilities</p>
                <p className="text-2xl font-bold">{stats.vulnerabilities}</p>
              </div>
              <div className="bg-red-500/20 p-3 rounded-lg">
                <Target className="w-6 h-6 text-red-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Threats</p>
                <p className="text-2xl font-bold">{stats.threats}</p>
              </div>
              <div className="bg-orange-500/20 p-3 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-orange-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Scans and Vulnerabilities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Scans */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Recent Security Scans
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow className="border-gray-700">
                  <TableHead className="text-gray-300">Scan Name</TableHead>
                  <TableHead className="text-gray-300">Type</TableHead>
                  <TableHead className="text-gray-300">Status</TableHead>
                  <TableHead className="text-gray-300">Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentScans.map((scan) => (
                  <TableRow key={scan.id} className="border-gray-700 hover:bg-gray-750">
                    <TableCell className="font-medium">{scan.name}</TableCell>
                    <TableCell className="text-gray-300">{scan.type}</TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(scan.status)}>
                        {scan.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-gray-300">{formatDate(scan.date)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Top Vulnerabilities */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5" />
              Top Vulnerabilities
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow className="border-gray-700">
                  <TableHead className="text-gray-300">Vulnerability</TableHead>
                  <TableHead className="text-gray-300">Severity</TableHead>
                  <TableHead className="text-gray-300">Status</TableHead>
                  <TableHead className="text-gray-300">Discovered</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {vulnerabilities.map((vuln) => (
                  <TableRow key={vuln.id} className="border-gray-700 hover:bg-gray-750">
                    <TableCell className="font-medium">{vuln.name}</TableCell>
                    <TableCell>
                      <Badge className={getSeverityColor(vuln.severity)}>
                        {vuln.severity}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant={vuln.status === 'resolved' ? 'default' : vuln.status === 'in_progress' ? 'secondary' : 'destructive'}>
                        {vuln.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-gray-300">{formatDate(vuln.discovered)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* Security Trends */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Security Trends
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 flex items-center justify-center text-gray-500">
            Security trend visualization would appear here
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-gray-800 border-gray-700 cursor-pointer hover:bg-gray-750 transition-colors">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Shield className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <h3 className="font-medium text-lg">Run Security Scan</h3>
                <p className="text-gray-400 text-sm">Scan your infrastructure for vulnerabilities</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700 cursor-pointer hover:bg-gray-750 transition-colors">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="bg-green-500/20 p-3 rounded-lg">
                <Lock className="w-6 h-6 text-green-400" />
              </div>
              <div>
                <h3 className="font-medium text-lg">Configure Security Policies</h3>
                <p className="text-gray-400 text-sm">Set up security rules and access controls</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700 cursor-pointer hover:bg-gray-750 transition-colors">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="bg-purple-500/20 p-3 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <h3 className="font-medium text-lg">Generate Report</h3>
                <p className="text-gray-400 text-sm">Create security compliance reports</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Security;