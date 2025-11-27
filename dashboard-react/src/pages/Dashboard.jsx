import React from 'react';
import { BiChip, BiMemoryCard, BiListUl, BiRefresh } from 'react-icons/bi';
import StatsCards from '@components/dashboard/StatsCards';
import MetricsChart from '@components/dashboard/MetricsChart';
import { useThemeStore } from '@store/themeStore';

const Dashboard = () => {
    const { isDark } = useThemeStore();

    const chartColor = isDark() ? '#03DAC6' : '#0F8B8D';
    const secondaryColor = isDark() ? '#0AFF99' : '#1C9B5B';
    const warningColor = isDark() ? '#FFB300' : '#FF9800';

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Stats Cards */}
            <StatsCards />

            {/* Metrics Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <MetricsChart
                    title="CPU Cluster Usage"
                    icon={BiChip}
                    color={chartColor}
                />
                <MetricsChart
                    title="Memory Usage"
                    icon={BiMemoryCard}
                    color={secondaryColor}
                />
                <MetricsChart
                    title="Queue Length"
                    icon={BiListUl}
                    color={warningColor}
                />
                <MetricsChart
                    title="Request Rate (RPS)"
                    icon={BiRefresh}
                    color={chartColor}
                />
            </div>

            {/* Additional sections can be added here */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Logs Terminal */}
                <div className="bg-light-panel dark:bg-dark-panel rounded-2xl p-6 border border-light-border dark:border-dark-border">
                    <h3 className="text-sm font-semibold uppercase tracking-wider text-light-text-secondary dark:text-dark-text-secondary mb-4">
                        System Logs
                    </h3>
                    <div className="bg-black dark:bg-black rounded-lg p-4 h-96 overflow-y-auto font-mono text-xs text-success-dark">
                        <div className="space-y-1">
                            <div>[18:45:32] [INFO] Node health check completed</div>
                            <div>[18:45:28] [INFO] Processing batch job #47283</div>
                            <div>[18:45:24] [INFO] Cache hit ratio: 94.2%</div>
                            <div>[18:45:20] [WARN] Queue consumer lag: 142ms</div>
                            <div>[18:45:16] [INFO] Workflow execution completed</div>
                        </div>
                    </div>
                </div>

                {/* Events Timeline */}
                <div className="bg-light-panel dark:bg-dark-panel rounded-2xl p-6 border border-light-border dark:border-dark-border">
                    <h3 className="text-sm font-semibold uppercase tracking-wider text-light-text-secondary dark:text-dark-text-secondary mb-4">
                        Events Timeline
                    </h3>
                    <div className="space-y-4">
                        {[
                            { time: '18:35:42', event: 'Node B1 latency spike detected' },
                            { time: '18:32:15', event: 'Team A scaling: 45 → 47 nodes' },
                            { time: '18:28:03', event: 'Queue threshold reached' },
                            { time: '18:21:37', event: 'Backup completed: 2.4 GB' },
                        ].map((item, idx) => (
                            <div key={idx} className="flex gap-3">
                                <div className="text-xs font-mono text-light-accent dark:text-dark-accent">
                                    {item.time}
                                </div>
                                <div className="text-sm">{item.event}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
