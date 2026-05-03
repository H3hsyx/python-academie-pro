import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react';

type ThemeContextValue = { theme: 'light' | 'dark'; toggleTheme: () => void };
const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => (localStorage.getItem('python_academie_theme') as 'light' | 'dark') || 'light');

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('python_academie_theme', theme);
  }, [theme]);

  const value = useMemo(() => ({ theme, toggleTheme: () => setTheme((current) => (current === 'light' ? 'dark' : 'light')) }), [theme]);
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) throw new Error('useTheme doit etre utilise dans ThemeProvider');
  return value;
}
