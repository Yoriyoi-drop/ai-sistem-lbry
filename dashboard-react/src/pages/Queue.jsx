import React, { useState } from 'react';
import axios from 'axios';

const QueuePage = () => {
  const [activeTab, setActiveTab] = useState('tasks');
  const [tasks, setTasks] = useState([
    {
      id: 1,
      type: 'Security Scan',
      priority: 'High',
      status: 'Processing',
      created: '2 hours ago',
      estimatedTime: '15 min',
      source: 'API Endpoint Monitoring'
    },
    {
      id: 2,
      type: 'Threat Analysis',
      priority: 'Critical',
      status: 'Queued',
      created: '1 hour ago',
      estimatedTime: '5 min',
      source: 'Network Traffic'
    },
    {
      id: 3,
      type: 'Data Classification',
      priority: 'Medium',
      status: 'Completed',
      created: '3 hours ago',
      estimatedTime: 'N/A',
      source: 'File Upload'
    },
    {
      id: 4,
      type: 'Behavioral Analysis',
      priority: 'Low',
      status: 'Processing',
      created: '30 minutes ago',
      estimatedTime: '45 min',
      source: 'User Activity'
    }
  ]);
  const [newTask, setNewTask] = useState({
    type: 'Security Scan',
    priority: 'Medium',
    source: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handlePauseQueue = async () => {
    setLoading(true);
    setMessage('Pausing queue...');

    try {
      // Simulate API call to pause queue
      await new Promise(resolve => setTimeout(resolve, 1000));
      setMessage('Queue paused successfully');
    } catch (error) {
      setMessage('Failed to pause queue');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async () => {
    if (!newTask.source) {
      setMessage('Please enter a source for the new task');
      return;
    }

    setLoading(true);
    setMessage('Adding new task...');

    try {
      // Simulate API call to add task
      await new Promise(resolve => setTimeout(resolve, 800));

      const newTaskObj = {
        id: tasks.length + 1,
        type: newTask.type,
        priority: newTask.priority,
        status: 'Queued',
        created: 'Just now',
        estimatedTime: 'Pending',
        source: newTask.source
      };

      setTasks([...tasks, newTaskObj]);
      setNewTask({ type: 'Security Scan', priority: 'Medium', source: '' });
      setMessage('Task added successfully');
    } catch (error) {
      setMessage('Failed to add task');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskAction = async (taskId, action) => {
    setLoading(true);

    try {
      // Simulate API call to perform task action
      await new Promise(resolve => setTimeout(resolve, 800));

      if (action === 'pause') {
        setMessage(`Task ${taskId} paused`);
        setTasks(tasks.map(task =>
          task.id === taskId ? { ...task, status: 'Paused' } : task
        ));
      } else if (action === 'cancel') {
        setMessage(`Task ${taskId} canceled`);
        setTasks(tasks.map(task =>
          task.id === taskId ? { ...task, status: 'Cancelled' } : task
        ));
      } else if (action === 'replay') {
        setMessage(`Task ${taskId} replayed`);
        setTasks(tasks.map(task =>
          task.id === taskId ? { ...task, status: 'Queued', created: 'Just now' } : task
        ));
      }
    } catch (error) {
      setMessage(`Failed to ${action} task`);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = async () => {
    setLoading(true);
    setMessage('Saving configuration...');

    try {
      // Simulate API call to save settings
      await new Promise(resolve => setTimeout(resolve, 1000));
      setMessage('Configuration saved successfully');
    } catch (error) {
      setMessage('Failed to save configuration');
    } finally {
      setLoading(false);
    }
  };

  // Calculate task statistics
  const totalTasks = tasks.length;
  const processingTasks = tasks.filter(t => t.status === 'Processing').length;
  const queuedTasks = tasks.filter(t => t.status === 'Queued').length;
  const completedTasks = tasks.filter(t => t.status === 'Completed').length;
  const pausedTasks = tasks.filter(t => t.status === 'Paused').length;
  const cancelledTasks = tasks.filter(t => t.status === 'Cancelled').length;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Message Queue</h1>

      {message && (
        <div className={`mb-4 p-3 rounded-md ${
          message.includes('successfully') ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' :
          message.includes('Failed') || message.includes('failed') ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' :
          message.includes('adding') || message.includes('pausing') || message.includes('saving') ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100' :
          'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100'
        }`}>
          {message}
        </div>
      )}

      {loading && (
        <div className="flex justify-center items-center mb-6">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'tasks' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('tasks')}
        >
          Task Queue
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'stats' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('stats')}
        >
          Statistics
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'settings' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('settings')}
        >
          Queue Settings
        </button>
      </div>

      {/* Task Queue */}
      {activeTab === 'tasks' && (
        <div>
          {/* Add New Task Form */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Add New Task</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Task Type</label>
                <select
                  value={newTask.type}
                  onChange={(e) => setNewTask({...newTask, type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="Security Scan">Security Scan</option>
                  <option value="Threat Analysis">Threat Analysis</option>
                  <option value="Data Classification">Data Classification</option>
                  <option value="Behavioral Analysis">Behavioral Analysis</option>
                  <option value="Vulnerability Assessment">Vulnerability Assessment</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Priority</label>
                <select
                  value={newTask.priority}
                  onChange={(e) => setNewTask({...newTask, priority: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                  <option value="Critical">Critical</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Source</label>
                <input
                  type="text"
                  value={newTask.source}
                  onChange={(e) => setNewTask({...newTask, source: e.target.value})}
                  placeholder="Enter source (e.g., API endpoint)"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div className="mt-4 flex justify-end">
              <button
                onClick={handleAddTask}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
              >
                Add Task
              </button>
            </div>
          </div>

          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white">Active Tasks</h2>
            <div className="flex space-x-3">
              <button
                onClick={handlePauseQueue}
                disabled={loading}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors disabled:opacity-50"
              >
                Pause Queue
              </button>
              <button
                onClick={() => document.querySelector('input[placeholder="Enter source (e.g., API endpoint)"]').focus()}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              >
                Add Task
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Task</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Priority</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Created</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Estimated Time</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Source</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {tasks.map((task) => (
                  <tr key={task.id} className={task.status === 'Completed' || task.status === 'Cancelled' ? 'bg-gray-50 dark:bg-gray-700' : ''}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">Task #{task.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{task.type}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        task.priority === 'Critical' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' :
                        task.priority === 'High' ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100' :
                        task.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100' :
                        'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                      }`}>
                        {task.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        task.status === 'Processing' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100' :
                        task.status === 'Queued' ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100' :
                        task.status === 'Paused' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100' :
                        task.status === 'Cancelled' ? 'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-200' :
                        'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                      }`}>
                        {task.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{task.created}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{task.estimatedTime}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{task.source}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {task.status !== 'Completed' && task.status !== 'Cancelled' ? (
                        <>
                          <button
                            onClick={() => handleTaskAction(task.id, 'pause')}
                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 mr-3"
                            disabled={loading}
                          >
                            Pause
                          </button>
                          <button
                            onClick={() => handleTaskAction(task.id, 'cancel')}
                            className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                            disabled={loading}
                          >
                            Cancel
                          </button>
                        </>
                      ) : task.status === 'Completed' ? (
                        <button
                          onClick={() => handleTaskAction(task.id, 'replay')}
                          className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                          disabled={loading}
                        >
                          Replay
                        </button>
                      ) : (
                        <span className="text-gray-400 dark:text-gray-500">N/A</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Task Summary */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mt-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Total Tasks</h3>
              <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{totalTasks}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Processing</h3>
              <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{processingTasks}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Queued</h3>
              <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">{queuedTasks}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Completed</h3>
              <p className="text-3xl font-bold text-green-600 dark:text-green-400">{completedTasks}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Paused/Cancelled</h3>
              <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{pausedTasks + cancelledTasks}</p>
            </div>
          </div>
        </div>
      )}

      {/* Statistics */}
      {activeTab === 'stats' && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-6">Queue Statistics</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Throughput</h3>
                <div className="h-48 flex items-center justify-center border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div className="text-center">
                    <p className="text-gray-500 dark:text-gray-400 mb-2">Tasks Processed Per Hour</p>
                    <p className="text-3xl font-bold text-gray-800 dark:text-white">142</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Processing Time</h3>
                <div className="h-48 flex items-center justify-center border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div className="text-center">
                    <p className="text-gray-500 dark:text-gray-400 mb-2">Average Processing Time</p>
                    <p className="text-3xl font-bold text-gray-800 dark:text-white">2.3 min</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Priority Distribution</h3>
                <div className="h-48 flex items-center justify-center border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div className="text-center">
                    <p className="text-gray-500 dark:text-gray-400 mb-2">Task Priority Breakdown</p>
                    <div className="flex flex-col items-start space-y-2 mt-4">
                      <div className="flex items-center">
                        <div className="w-4 h-4 bg-red-500 mr-2"></div>
                        <span className="text-sm">Critical: {tasks.filter(t => t.priority === 'Critical').length}</span>
                      </div>
                      <div className="flex items-center">
                        <div className="w-4 h-4 bg-orange-500 mr-2"></div>
                        <span className="text-sm">High: {tasks.filter(t => t.priority === 'High').length}</span>
                      </div>
                      <div className="flex items-center">
                        <div className="w-4 h-4 bg-yellow-500 mr-2"></div>
                        <span className="text-sm">Medium: {tasks.filter(t => t.priority === 'Medium').length}</span>
                      </div>
                      <div className="flex items-center">
                        <div className="w-4 h-4 bg-green-500 mr-2"></div>
                        <span className="text-sm">Low: {tasks.filter(t => t.priority === 'Low').length}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Queue Health</h3>
                <div className="h-48 flex items-center justify-center border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div className="text-center">
                    <p className="text-gray-500 dark:text-gray-400 mb-2">Queue Status</p>
                    <p className="text-3xl font-bold text-green-600 dark:text-green-400">Healthy</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Queue Settings */}
      {activeTab === 'settings' && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-6">Queue Configuration</h2>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Maximum Concurrent Tasks
              </label>
              <input
                type="number"
                defaultValue="5"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Queue Priority Strategy
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                <option>Priority-based (Critical &gt; High &gt; Medium &gt; Low)</option>
                <option>First In, First Out (FIFO)</option>
                <option>Round Robin</option>
                <option>Load-based</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Retry Attempts
              </label>
              <input
                type="number"
                defaultValue="3"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Maximum Queue Size
              </label>
              <input
                type="number"
                defaultValue="1000"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div className="flex items-center">
              <input
                id="auto-scaling"
                type="checkbox"
                defaultChecked={true}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
              />
              <label htmlFor="auto-scaling" className="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Enable auto-scaling based on queue load
              </label>
            </div>

            <div className="flex justify-end">
              <button
                onClick={handleSaveSettings}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
              >
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default QueuePage;