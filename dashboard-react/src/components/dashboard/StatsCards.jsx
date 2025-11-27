import React from 'react';
import { motion } from 'framer-motion';
import { BiChip, BiServer, BiShieldAlt, BiAnalyse, BiListUl } from 'react-icons/bi';
import { useDashboardStore } from '@store/dashboardStore';

const StatsCard = ({ title, value, subtitle, status, icon: Icon }) => {
    const statusColors = {
        success: 'bg-success-light dark:bg-success-dark',
        warning: 'bg-warning-light dark:bg-warning-dark',
        error: 'bg-error-light dark:bg-error-dark',
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ y: -4 }}
            className="card-hover bg-light-panel dark:bg-dark-panel rounded-2xl p-6 border border-light-border dark:border-dark-border"
        >
            <div className="flex justify-between items-start mb-3">
                <div className="text-xs font-semibold uppercase tracking-wider text-light-text-secondary dark:text-dark-text-secondary">
                    {title}
                </div>
                <Icon className="text-2xl opacity-50" />
            </div>

            <div className="flex items-center mb-2">
                <span className={`status-dot ${statusColors[status]} mr-2`} />
                <div className="text-4xl font-bold font-display">{value}</div>
            </div>

            <div className="text-xs text-light-text-secondary dark:text-dark-text-secondary">
                {subtitle}
            </div>
        </motion.div>
    );
};

const StatsCards = () => {
    const { stats } = useDashboardStore();

    const cards = [
        {
            title: 'Team A Status',
            value: `${stats.teamAHealth}%`,
            subtitle: 'Healthy · 47 nodes active',
            status: 'success',
            icon: BiChip,
        },
        {
            title: 'Team B Status',
            value: `${stats.teamBHealth}%`,
            subtitle: 'Healthy · 45 nodes active',
            status: 'success',
            icon: BiChip,
        },
        {
            title: 'Recovery Team',
            value: 'Standby',
            subtitle: 'Ready · 8 nodes available',
            status: 'warning',
            icon: BiShieldAlt,
        },
        {
            title: 'Nodes Running',
            value: stats.nodesRunning,
            subtitle: '↑ 12 since last hour',
            status: 'success',
            icon: BiServer,
        },
        {
            title: 'Avg Latency',
            value: `${stats.avgLatency}ms`,
            subtitle: '↓ 8ms improvement',
            status: 'success',
            icon: BiAnalyse,
        },
        {
            title: 'Queue Load',
            value: `${stats.queueLoad}%`,
            subtitle: '2,847 pending tasks',
            status: 'success',
            icon: BiListUl,
        },
    ];

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
            {cards.map((card, index) => (
                <StatsCard key={index} {...card} />
            ))}
        </div>
    );
};

export default StatsCards;
