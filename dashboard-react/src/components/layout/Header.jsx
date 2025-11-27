import React from 'react';
import { motion } from 'framer-motion';
import { FiSun, FiMoon, FiBell, FiMenu } from 'react-icons/fi';
import { useThemeStore } from '@store/themeStore';
import { useInterval } from 'react-use';
import { format } from 'date-fns';

const Header = ({ onMenuClick }) => {
    const { theme, toggleTheme } = useThemeStore();
    const [currentTime, setCurrentTime] = React.useState(new Date());

    useInterval(() => {
        setCurrentTime(new Date());
    }, 1000);

    return (
        <motion.header
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            className="fixed top-0 left-0 right-0 h-16 glass-effect bg-light-bg dark:bg-dark-bg border-b border-light-border dark:border-dark-border z-50"
        >
            <div className="h-full px-4 md:px-6 flex items-center justify-between">
                {/* Left Side */}
                <div className="flex items-center gap-4">
                    <button
                        onClick={onMenuClick}
                        className="lg:hidden p-2 hover:bg-light-panel dark:hover:bg-dark-panel rounded-lg transition-colors"
                    >
                        <FiMenu className="text-xl" />
                    </button>

                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-light-accent to-light-accent-secondary dark:from-dark-accent dark:to-dark-accent-secondary flex items-center justify-center text-white font-bold text-lg">
                            NF
                        </div>
                        <div className="font-display text-xl font-bold">NexaForge</div>
                    </div>
                </div>

                {/* Right Side */}
                <div className="flex items-center gap-3">
                    <button
                        onClick={toggleTheme}
                        className="p-2 hover:bg-light-panel dark:hover:bg-dark-panel rounded-lg transition-colors"
                        aria-label="Toggle theme"
                    >
                        <motion.div
                            initial={false}
                            animate={{ rotate: theme === 'dark' ? 0 : 180 }}
                            transition={{ duration: 0.3 }}
                        >
                            {theme === 'dark' ? (
                                <FiSun className="text-xl" />
                            ) : (
                                <FiMoon className="text-xl" />
                            )}
                        </motion.div>
                    </button>

                    <div className="hidden md:block font-mono text-sm text-light-text-secondary dark:text-dark-text-secondary">
                        {format(currentTime, 'HH:mm:ss')}
                    </div>

                    <button className="relative p-2 hover:bg-light-panel dark:hover:bg-dark-panel rounded-lg transition-colors">
                        <FiBell className="text-xl" />
                        <span className="absolute top-1 right-1 w-2 h-2 bg-error-light dark:bg-error-dark rounded-full animate-pulse" />
                    </button>
                </div>
            </div>
        </motion.header>
    );
};

export default Header;
