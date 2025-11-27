import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useThemeStore = create(
    persist(
        (set, get) => ({
            theme: 'dark',
            toggleTheme: () => set((state) => {
                const newTheme = state.theme === 'dark' ? 'light' : 'dark';
                document.documentElement.classList.remove('dark', 'light');
                document.documentElement.classList.add(newTheme);
                return { theme: newTheme };
            }),
            setTheme: (theme) => {
                document.documentElement.classList.remove('dark', 'light');
                document.documentElement.classList.add(theme);
                set({ theme });
            },
            isDark: () => get().theme === 'dark',
        }),
        {
            name: 'nexaforge-theme',
        }
    )
);
