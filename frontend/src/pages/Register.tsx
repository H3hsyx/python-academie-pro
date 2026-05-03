import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Card } from '../components/Card';

export function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    try {
      await register(form.username, form.email, form.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inscription');
    }
  }

  return (
    <div className="auth-page">
      <Card className="auth-card"><h1>Inscription</h1><p>Cree un compte pour suivre ta progression, gagner des XP et enregistrer tes favoris.</p><form onSubmit={submit} className="stack-form"><label>Nom utilisateur<input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></label><label>Email<input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label><label>Mot de passe<input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label><button className="btn btn-primary">Commencer</button>{error && <p className="error">{error}</p>}</form><p>Deja inscrit ? <Link to="/connexion">Connexion</Link></p></Card>
    </div>
  );
}
