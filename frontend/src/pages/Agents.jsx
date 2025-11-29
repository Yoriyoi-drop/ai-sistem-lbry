import React, { useState, useEffect } from 'react';
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
