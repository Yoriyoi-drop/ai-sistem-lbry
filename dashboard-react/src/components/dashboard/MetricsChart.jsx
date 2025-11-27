import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { useThemeStore } from '@store/themeStore';
import { useInterval } from 'react-use';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const MetricsChart = ({ title, icon: Icon, color }) => {
    const { isDark } = useThemeStore();
    const [data, setData] = React.useState({
        labels: Array(20).fill(''),
        datasets: [
            {
                label: title,
                data: Array(20).fill(0).map(() => Math.random() * 100),
                borderColor: color,
                backgroundColor: `${color}20`,
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 4,
            },
        ],
    });

    useInterval(() => {
        setData((prev) => ({
            ...prev,
            datasets: [
                {
                    ...prev.datasets[0],
                    data: [...prev.datasets[0].data.slice(1), Math.random() * 100],
                },
            ],
        }));
    }, 2000);

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: isDark() ? '#1A1A1A' : '#FFFFFF',
                titleColor: isDark() ? '#FFFFFF' : '#121212',
                bodyColor: isDark() ? '#B3B3B3' : '#333333',
                borderColor: color,
                borderWidth: 1,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                grid: {
                    color: isDark() ? '#2A2A2A' : '#E0E0E0',
                    drawBorder: false,
                },
                ticks: {
                    color: isDark() ? '#B3B3B3' : '#333333',
                },
            },
            x: {
                grid: { display: false },
                ticks: {
                    color: isDark() ? '#B3B3B3' : '#333333',
                },
            },
        },
        animation: {
            duration: 0,
        },
    };

    return (
        <div className="bg-light-panel dark:bg-dark-panel rounded-2xl p-6 border border-light-border dark:border-dark-border card-hover">
            <div className="flex justify-between items-center mb-4">
                <div className="flex items-center gap-2">
                    <Icon className="text-xl" />
                    <h3 className="text-sm font-semibold uppercase tracking-wider text-light-text-secondary dark:text-dark-text-secondary">
                        {title}
                    </h3>
                </div>
            </div>
            <div className="h-64">
                <Line data={data} options={options} />
            </div>
        </div>
    );
};

export default MetricsChart;
