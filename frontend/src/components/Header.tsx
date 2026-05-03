import { Link, NavLink, useNavigate } from 'react-router-dom';
import { Moon, Search, Sun, UserCircle } from 'lucide-react';
import { useState } from 'react';
import { navItems } from '../data/navigation';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../hooks/useTheme';

export function Header() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  function submit(event: React.FormEvent) {
    event.preventDefault();
    if (query.trim().length >= 2) navigate(`/recherche?q=${encodeURIComponent(query.trim())}`);
  }

  return (
    <header className="site-header">
      <Link to="/" className="brand"><span>Py</span> Academie</Link>
      <nav className="top-nav" aria-label="Navigation principale">
        {navItems.slice(1, 5).map((item) => <NavLink key={item.to} to={item.to}>{item.label}</NavLink>)}
      </nav>
      <form className="search" onSubmit={submit} role="search">
        <Search size={16} />
        <input aria-label="Recherche globale" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Cours, erreurs, projets..." />
      </form>
      <button className="icon-btn" onClick={toggleTheme} aria-label="Changer de theme">{theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}</button>
      {user ? (
        <div className="header-user">
          <Link to="/profil"><UserCircle size={18} /> {user.username}</Link>
          <button className="btn btn-ghost" onClick={logout}>Sortir</button>
        </div>
      ) : (
        <div className="header-user"><Link className="btn btn-ghost" to="/connexion">Connexion</Link><Link className="btn btn-primary" to="/inscription">Commencer</Link></div>
      )}
    </header>
  );
}
