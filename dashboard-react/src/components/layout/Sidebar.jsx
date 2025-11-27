import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
    BiGrid,
    BiNetworkChart,
    BiServer,
    BiGroup,
    BiChat,
    BiHdd,
    BiError,
    BiFile,
    BiCog,
    BiShield,
} from 'react-icons/bi';
import { clsx } from 'clsx';

const menuItems = [
    { icon: BiGrid, label: 'Dashboard', path: '/' },
    { icon: BiShield, label: 'SQL Injection', path: '/sql-injection' },
    { icon: BiShield, label: 'Advanced Security', path: '/advanced-security' },
    { icon: BiShield, label: 'Neural Security', path: '/neural-security' },
    { icon: BiShield, label: 'HF Security', path: '/hf-security' },
    { icon: BiNetworkChart, label: 'Workflows Graph', path: '/workflows' },
    { icon: BiServer, label: 'Node Status', path: '/nodes' },
    { icon: BiGroup, label: 'AI Teams', path: '/teams' },
    { icon: BiChat, label: 'Message Queue', path: '/queue' },
    { icon: BiHdd, label: 'Server Health', path: '/health' },
    { icon: BiError, label: 'Alerts', path: '/alerts' },
    { icon: BiFile, label: 'Logs', path: '/logs' },
    { icon: BiCog, label: 'Settings', path: '/settings' },
];

const Sidebar = ({ isOpen, onClose }) => {
    return (
        <>
            {/* Mobile Overlay */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="lg:hidden fixed inset-0 bg-black/50 z-40"
                    />
                )}
            </AnimatePresence>

            {/* Sidebar */}
            <motion.aside
                initial={{ x: -260 }}
                animate={{ x: isOpen ? 0 : -260 }}
                className={clsx(
                    'fixed top-16 left-0 bottom-0 w-64 bg-light-panel dark:bg-dark-panel border-r border-light-border dark:border-dark-border z-40 flex-shrink-0',
                    'lg:static lg:translate-x-0 lg:left-0 transition-transform duration-300'
                )}
            >
                <nav className="p-4 space-y-1">
                    {menuItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            onClick={() => onClose()}
                            className={({ isActive }) =>
                                clsx(
                                    'flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200',
                                    'border-l-3 border-transparent',
                                    isActive
                                        ? 'bg-light-accent/10 dark:bg-dark-accent/10 border-l-light-accent dark:border-l-dark-accent text-light-accent dark:text-dark-accent'
                                        : 'hover:bg-light-bg dark:hover:bg-dark-bg text-light-text-secondary dark:text-dark-text-secondary hover:text-light-text dark:hover:text-dark-text'
                                )
                            }
                        >
                            <item.icon className="text-xl flex-shrink-0" />
                            <span className="text-sm font-medium">{item.label}</span>
                        </NavLink>
                    ))}
                </nav>
            </motion.aside>


        </>
    );
};

export default Sidebar;
