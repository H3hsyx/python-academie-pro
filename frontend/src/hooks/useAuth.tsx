import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react';
import { api, clearToken, getToken } from '../api/client';
import type { User } from '../api/types';

type AuthContextValue = {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  async function refresh() {
    if (!getToken()) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const me = await api.get<User>('/auth/me');
      setUser(me);
    } catch {
      clearToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function login(email: string, password: string) {
    await api.login(email, password);
    await refresh();
  }

  async function register(username: string, email: string, password: string) {
    await api.post<User>('/auth/register', { username, email, password });
    await login(email, password);
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  const value = useMemo(() => ({ user, loading, login, register, logout, refresh }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth doit etre utilise dans AuthProvider');
  return value;
}
