/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                // Border color for default usage (will be light border by default)
                border: '#E0E0E0', // Light mode default
                // Dark Mode Colors
                dark: {
                    bg: '#0D0D0D',
                    panel: '#1A1A1A',
                    text: '#FFFFFF',
                    'text-secondary': '#B3B3B3',
                    accent: '#03DAC6',
                    'accent-secondary': '#0AFF99',
                    border: '#2A2A2A',
                },
                // Light Mode Colors
                light: {
                    bg: '#FFFFFF',
                    panel: '#F5F5F5',
                    text: '#121212',
                    'text-secondary': '#333333',
                    accent: '#0F8B8D',
                    'accent-secondary': '#1C9B5B',
                    border: '#E0E0E0',
                },
                // Status Colors
                success: {
                    dark: '#0AFF99',
                    light: '#1C9B5B',
                },
                warning: {
                    dark: '#FFB300',
                    light: '#FF9800',
                },
                error: {
                    dark: '#FF2D55',
                    light: '#D7263D',
                },
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                display: ['Sora', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'fade-in': 'fadeIn 0.3s ease-in-out',
                'slide-in': 'slideIn 0.3s ease-out',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideIn: {
                    '0%': { transform: 'translateY(-10px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
            },
        },
    },
    plugins: [],
}
