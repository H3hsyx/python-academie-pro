import { NavLink } from 'react-router-dom';
import { navItems } from '../data/navigation';

export function Sidebar() {
  return (
    <aside className="sidebar" aria-label="Navigation secondaire">
      <div className="sidebar-section">
        <span className="sidebar-title">Plateforme</span>
        {navItems.map((item) => <NavLink key={item.to} to={item.to}>{item.label}</NavLink>)}
      </div>
      <div className="sidebar-callout">
        <strong>Objectif semaine</strong>
        <p>3 lecons, 5 exercices, 1 mini-projet.</p>
      </div>
    </aside>
  );
}
