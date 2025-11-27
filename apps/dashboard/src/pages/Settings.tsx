import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle
} from '../components/ui/card';
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
  Label
} from '../components/ui/label';

const Settings = () => {
  const [userSettings, setUserSettings] = useState({
    email: 'user@example.com',
    username: 'user123',
    theme: 'dark',
    notifications: true,
    twoFactor: false
  });

  const [securitySettings, setSecuritySettings] = useState({
    passwordExpiry: 90,
    sessionTimeout: 30,
    loginAttempts: 5,
    apiRateLimit: 100
  });

  const [labyrinthSettings, setLabyrinthSettings] = useState({
    complexity: 5,
    detectionSensitivity: 'medium',
    decoyNodes: 10,
    routeObfuscation: true
  });

  const handleSave = () => {
    // Save settings logic would go here
    console.log('Settings saved:', { userSettings, securitySettings, labyrinthSettings });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-gray-400 mt-1">Manage your account and security settings</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Profile Settings */}
        <Card className="bg-gray-800 border-gray-700 lg:col-span-2">
          <CardHeader>
            <CardTitle>User Profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  value={userSettings.email}
                  onChange={(e) => setUserSettings({...userSettings, email: e.target.value})}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              <div>
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  value={userSettings.username}
                  onChange={(e) => setUserSettings({...userSettings, username: e.target.value})}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="theme">Theme</Label>
                <Select value={userSettings.theme} onValueChange={(value) => setUserSettings({...userSettings, theme: value})}>
                  <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-gray-800 border-gray-700">
                    <SelectItem value="light">Light</SelectItem>
                    <SelectItem value="dark">Dark</SelectItem>
                    <SelectItem value="system">System</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Notification Preferences</Label>
                <div className="flex items-center space-x-2 mt-2">
                  <input
                    type="checkbox"
                    id="notifications"
                    checked={userSettings.notifications}
                    onChange={(e) => setUserSettings({...userSettings, notifications: e.target.checked})}
                    className="h-4 w-4 rounded border-gray-600 bg-gray-700 text-blue-600 focus:ring-blue-500"
                  />
                  <Label htmlFor="notifications" className="text-gray-300">Enable email notifications</Label>
                </div>
              </div>
            </div>

            <div>
              <Label>Security</Label>
              <div className="flex items-center space-x-2 mt-2">
                <input
                  type="checkbox"
                  id="twoFactor"
                  checked={userSettings.twoFactor}
                  onChange={(e) => setUserSettings({...userSettings, twoFactor: e.target.checked})}
                  className="h-4 w-4 rounded border-gray-600 bg-gray-700 text-blue-600 focus:ring-blue-500"
                />
                <Label htmlFor="twoFactor" className="text-gray-300">Enable two-factor authentication</Label>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Security Settings */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle>Security Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="passwordExpiry">Password Expiry (days)</Label>
              <Input
                id="passwordExpiry"
                type="number"
                value={securitySettings.passwordExpiry}
                onChange={(e) => setSecuritySettings({...securitySettings, passwordExpiry: parseInt(e.target.value)})}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>
            <div>
              <Label htmlFor="sessionTimeout">Session Timeout (minutes)</Label>
              <Input
                id="sessionTimeout"
                type="number"
                value={securitySettings.sessionTimeout}
                onChange={(e) => setSecuritySettings({...securitySettings, sessionTimeout: parseInt(e.target.value)})}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>
            <div>
              <Label htmlFor="loginAttempts">Max Login Attempts</Label>
              <Input
                id="loginAttempts"
                type="number"
                value={securitySettings.loginAttempts}
                onChange={(e) => setSecuritySettings({...securitySettings, loginAttempts: parseInt(e.target.value)})}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>
            <div>
              <Label htmlFor="apiRateLimit">API Rate Limit (requests/minute)</Label>
              <Input
                id="apiRateLimit"
                type="number"
                value={securitySettings.apiRateLimit}
                onChange={(e) => setSecuritySettings({...securitySettings, apiRateLimit: parseInt(e.target.value)})}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>
          </CardContent>
        </Card>

        {/* Labyrinth Settings */}
        <Card className="bg-gray-800 border-gray-700 lg:col-span-3">
          <CardHeader>
            <CardTitle>Labyrinth Security Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <Label htmlFor="complexity">Labyrinth Complexity</Label>
                <Input
                  id="complexity"
                  type="number"
                  min="1"
                  max="10"
                  value={labyrinthSettings.complexity}
                  onChange={(e) => setLabyrinthSettings({...labyrinthSettings, complexity: parseInt(e.target.value)})}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              <div>
                <Label htmlFor="sensitivity">Detection Sensitivity</Label>
                <Select 
                  value={labyrinthSettings.detectionSensitivity} 
                  onValueChange={(value) => setLabyrinthSettings({...labyrinthSettings, detectionSensitivity: value})}
                >
                  <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-gray-800 border-gray-700">
                    <SelectItem value="low">Low</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="very_high">Very High</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="decoyNodes">Number of Decoy Nodes</Label>
                <Input
                  id="decoyNodes"
                  type="number"
                  value={labyrinthSettings.decoyNodes}
                  onChange={(e) => setLabyrinthSettings({...labyrinthSettings, decoyNodes: parseInt(e.target.value)})}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              <div>
                <Label>Route Obfuscation</Label>
                <div className="flex items-center space-x-2 mt-2">
                  <input
                    type="checkbox"
                    id="routeObfuscation"
                    checked={labyrinthSettings.routeObfuscation}
                    onChange={(e) => setLabyrinthSettings({...labyrinthSettings, routeObfuscation: e.target.checked})}
                    className="h-4 w-4 rounded border-gray-600 bg-gray-700 text-blue-600 focus:ring-blue-500"
                  />
                  <Label htmlFor="routeObfuscation" className="text-gray-300">Enable</Label>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="lg:col-span-3">
          <Button 
            onClick={handleSave}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-2"
          >
            Save Settings
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Settings;