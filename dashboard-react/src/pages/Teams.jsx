import React, { useState } from 'react';
import axios from 'axios';

const TeamsPage = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [teams, setTeams] = useState([
    {
      id: 1,
      name: 'Security Research Team',
      members: 5,
      status: 'Active',
      lastActivity: '2 hours ago',
      description: 'Researches new security threats and vulnerabilities'
    },
    {
      id: 2,
      name: 'Threat Detection Team',
      members: 8,
      status: 'Active',
      lastActivity: '30 minutes ago',
      description: 'Develops and maintains threat detection algorithms'
    },
    {
      id: 3,
      name: 'Response Automation Team',
      members: 6,
      status: 'Paused',
      lastActivity: '1 day ago',
      description: 'Creates automated response mechanisms for threats'
    }
  ]);
  const [members, setMembers] = useState([
    { id: 1, name: 'Alice Johnson', role: 'Lead Security Engineer', status: 'Online', team: 'Security Research Team' },
    { id: 2, name: 'Bob Chen', role: 'Threat Analyst', status: 'Online', team: 'Threat Detection Team' },
    { id: 3, name: 'Carol Davis', role: 'AI Specialist', status: 'Offline', team: 'Threat Detection Team' },
    { id: 4, name: 'David Wilson', role: 'DevSecOps', status: 'Online', team: 'Response Automation Team' },
  ]);
  const [newTeam, setNewTeam] = useState({ name: '', description: '' });
  const [newMember, setNewMember] = useState({ name: '', role: '', team: 'Security Research Team' });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleCreateTeam = async () => {
    if (!newTeam.name) {
      setMessage('Please enter a team name');
      return;
    }

    setLoading(true);
    setMessage('Creating new team...');

    try {
      await new Promise(resolve => setTimeout(resolve, 1000));

      const newTeamObj = {
        id: teams.length + 1,
        name: newTeam.name,
        members: 0,
        status: 'Active',
        lastActivity: 'Just now',
        description: newTeam.description || 'New security team'
      };

      setTeams([...teams, newTeamObj]);
      setNewTeam({ name: '', description: '' });
      setMessage('Team created successfully');
    } catch (error) {
      setMessage('Failed to create team');
    } finally {
      setLoading(false);
    }
  };

  const handleAddMember = async () => {
    if (!newMember.name || !newMember.role) {
      setMessage('Please enter name and role for the new member');
      return;
    }

    setLoading(true);
    setMessage('Adding new member...');

    try {
      await new Promise(resolve => setTimeout(resolve, 800));

      const newMemberObj = {
        id: members.length + 1,
        name: newMember.name,
        role: newMember.role,
        status: 'Online',
        team: newMember.team
      };

      setMembers([...members, newMemberObj]);
      setNewMember({ name: '', role: '', team: 'Security Research Team' });
      setMessage('Member added successfully');
    } catch (error) {
      setMessage('Failed to add member');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTeamStatus = async (teamId) => {
    setLoading(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 500));

      setTeams(teams.map(team =>
        team.id === teamId
          ? {
              ...team,
              status: team.status === 'Active' ? 'Paused' : 'Active',
              lastActivity: 'Just now'
            }
          : team
      ));

      setMessage(`Team ${teamId} status updated`);
    } catch (error) {
      setMessage('Failed to update team status');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMember = async (memberId) => {
    setLoading(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 500));

      setMembers(members.filter(member => member.id !== memberId));
      setMessage('Member removed successfully');
    } catch (error) {
      setMessage('Failed to remove member');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">AI Teams Management</h1>

      {message && (
        <div className={`mb-4 p-3 rounded-md ${
          message.includes('successfully') ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' :
          message.includes('Failed') || message.includes('failed') ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' :
          message.includes('creating') || message.includes('adding') || message.includes('updating') ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100' :
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
          className={`px-4 py-2 font-medium ${activeTab === 'overview' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('overview')}
        >
          Teams Overview
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'members' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('members')}
        >
          Team Members
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'activity' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('activity')}
        >
          Activity
        </button>
      </div>

      {/* Teams Overview */}
      {activeTab === 'overview' && (
        <div>
          {/* Create New Team Form */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Create New Team</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Team Name</label>
                <input
                  type="text"
                  value={newTeam.name}
                  onChange={(e) => setNewTeam({...newTeam, name: e.target.value})}
                  placeholder="Enter team name"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
                <input
                  type="text"
                  value={newTeam.description}
                  onChange={(e) => setNewTeam({...newTeam, description: e.target.value})}
                  placeholder="Enter team description"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
            <div className="mt-4 flex justify-end">
              <button
                onClick={handleCreateTeam}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
              >
                Create Team
              </button>
            </div>
          </div>

          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white">AI Security Teams</h2>
            <button
              onClick={() => document.querySelector('input[placeholder="Enter team name"]').focus()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
              Create New Team
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {teams.map((team) => (
              <div key={team.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-medium text-gray-800 dark:text-white">{team.name}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    team.status === 'Active'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                      : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100'
                  }`}>
                    {team.status}
                  </span>
                </div>

                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">{team.description}</p>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500 dark:text-gray-400">Members:</span>
                    <span className="text-gray-800 dark:text-white font-medium">{team.members}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500 dark:text-gray-400">Last Activity:</span>
                    <span className="text-gray-800 dark:text-white font-medium">{team.lastActivity}</span>
                  </div>
                </div>

                <div className="flex space-x-2">
                  <button
                    onClick={() => setActiveTab('members')}
                    className="flex-1 px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white text-sm rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                  >
                    View
                  </button>
                  <button
                    onClick={() => handleToggleTeamStatus(team.id)}
                    disabled={loading}
                    className="flex-1 px-3 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded-md hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors disabled:opacity-50"
                  >
                    {team.status === 'Active' ? 'Pause' : 'Resume'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Team Members */}
      {activeTab === 'members' && (
        <div>
          {/* Add New Member Form */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Add New Member</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Name</label>
                <input
                  type="text"
                  value={newMember.name}
                  onChange={(e) => setNewMember({...newMember, name: e.target.value})}
                  placeholder="Enter member name"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
                <input
                  type="text"
                  value={newMember.role}
                  onChange={(e) => setNewMember({...newMember, role: e.target.value})}
                  placeholder="Enter role"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Team</label>
                <select
                  value={newMember.team}
                  onChange={(e) => setNewMember({...newMember, team: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  {teams.map(team => (
                    <option key={team.id} value={team.name}>{team.name}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="mt-4 flex justify-end">
              <button
                onClick={handleAddMember}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
              >
                Add Member
              </button>
            </div>
          </div>

          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white">Team Members</h2>
            <button
              onClick={() => document.querySelector('input[placeholder="Enter member name"]').focus()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
              Add Member
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Member</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Role</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Team</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {members.map((member) => (
                  <tr key={member.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
                            {member.name.split(' ').map(n => n[0]).join('')}
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">{member.name}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{member.role}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{member.team}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        member.status === 'Online'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                          : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                      }`}>
                        {member.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      <button
                        className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 mr-3"
                        disabled={loading}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleRemoveMember(member.id)}
                        disabled={loading}
                        className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Activity */}
      {activeTab === 'activity' && (
        <div>
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-6">Recent Activity</h2>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
                    AJ
                  </div>
                </div>
                <div className="ml-4">
                  <h4 className="text-sm font-medium text-gray-800 dark:text-white">Alice Johnson completed threat analysis</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">2 hours ago</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center text-white font-bold">
                    BC
                  </div>
                </div>
                <div className="ml-4">
                  <h4 className="text-sm font-medium text-gray-800 dark:text-white">Bob Chen detected potential XSS vulnerability</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">3 hours ago</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-bold">
                    DW
                  </div>
                </div>
                <div className="ml-4">
                  <h4 className="text-sm font-medium text-gray-800 dark:text-white">David Wilson updated response automation rules</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">1 day ago</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-yellow-500 flex items-center justify-center text-white font-bold">
                    CD
                  </div>
                </div>
                <div className="ml-4">
                  <h4 className="text-sm font-medium text-gray-800 dark:text-white">Carol Davis finished research on new attack vectors</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">2 days ago</p>
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
                View Full Activity Log
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeamsPage;