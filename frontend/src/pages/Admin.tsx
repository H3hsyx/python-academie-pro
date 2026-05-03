import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { Card } from '../components/Card';

export function Admin() {
  const [stats, setStats] = useState<Record<string, number>>({});
  const [users, setUsers] = useState<any[]>([]);
  const [courseTitle, setCourseTitle] = useState('');
  const [message, setMessage] = useState('');

  async function load() {
    setStats(await api.get<Record<string, number>>('/admin/stats'));
    setUsers(await api.get<any[]>('/admin/users'));
  }
  useEffect(() => { load().catch(console.error); }, []);

  async function createCourse() {
    try {
      await api.post('/admin/courses', { title: courseTitle, description: 'Nouveau parcours ajoute depuis le panel admin.', level: 'Debutant' });
      setCourseTitle('');
      setMessage('Parcours cree.');
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Erreur');
    }
  }

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">Administration</span><h1>Panel administrateur</h1><p>Ajouter des contenus, gerer les utilisateurs et moderer les commentaires.</p></div></div>
      <section className="stats-grid">{Object.entries(stats).map(([key, value]) => <Card key={key}><strong>{value}</strong><span>{key}</span></Card>)}</section>
      <section className="section-grid two">
        <Card><h2>Ajouter un parcours</h2><input value={courseTitle} onChange={(e) => setCourseTitle(e.target.value)} placeholder="Titre du parcours" /><button className="btn btn-primary" onClick={createCourse}>Creer</button>{message && <p className="notice">{message}</p>}</Card>
        <Card><h2>Utilisateurs</h2><div className="table"><table><tbody>{users.slice(0, 10).map((user) => <tr key={user.id}><td>{user.username}</td><td>{user.email}</td><td>{user.role}</td><td>{user.xp} XP</td></tr>)}</tbody></table></div></Card>
      </section>
      <Card><h2>Actions prevues</h2><ul><li>Ajouter, modifier, supprimer des cours.</li><li>Ajouter exercices, quiz, projets et ressources.</li><li>Voir les statistiques de progression.</li><li>Moderer les commentaires et discussions.</li></ul></Card>
    </div>
  );
}
