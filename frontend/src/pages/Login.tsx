import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Card } from '../components/Card';

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: 'demo@python.local', password: 'Demo123!' });
  const [error, setError] = useState('');

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    try {
      await login(form.email, form.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur de connexion');
    }
  }

  return (
    <div className="auth-page">
      <Card className="auth-card"><h1>Connexion</h1><p>Compte demo: demo@python.local / Demo123!</p><form onSubmit={submit} className="stack-form"><label>Email<input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label><label>Mot de passe<input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label><button className="btn btn-primary">Connexion</button>{error && <p className="error">{error}</p>}</form><p>Pas de compte ? <Link to="/inscription">Inscription</Link></p></Card>
    </div>
  );
}
