import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

export function Layout() {
  return (
    <div>
      <Header />
      <div className="app-shell">
        <Sidebar />
        <main className="main-content"><Outlet /></main>
      </div>
      <footer className="footer">
        <div><strong>Python Academie Pro</strong><p>Apprendre Python serieusement, de zero au niveau avance.</p></div>
        <div><a href="/ressources">Ressources</a><a href="/communaute">Communaute</a><a href="/parcours">Parcours</a></div>
      </footer>
    </div>
  );
}
