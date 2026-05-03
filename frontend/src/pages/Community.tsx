import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { Card } from '../components/Card';

export function Community() {
  const [discussions, setDiscussions] = useState<any[]>([]);
  const [form, setForm] = useState({ title: '', body: '', theme: 'general' });
  const [message, setMessage] = useState('');

  async function load() {
    const data = await api.get<any[]>('/community/discussions');
    setDiscussions(data);
  }
  useEffect(() => { load().catch(console.error); }, []);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    try {
      await api.post('/community/discussions', form);
      setForm({ title: '', body: '', theme: 'general' });
      setMessage('Discussion publiee.');
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Connexion requise');
    }
  }

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">Questions, projets, defis</span><h1>Communaute</h1><p>Pose des questions, partage tes projets, participe aux defis hebdomadaires.</p></div></div>
      <section className="section-grid two">
        <Card><h2>Nouvelle discussion</h2><form onSubmit={submit} className="stack-form"><input placeholder="Titre" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /><textarea placeholder="Message" value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} /><input placeholder="Theme" value={form.theme} onChange={(e) => setForm({ ...form, theme: e.target.value })} /><button className="btn btn-primary">Publier</button>{message && <p className="notice">{message}</p>}</form></Card>
        <Card><h2>Defis hebdomadaires</h2><p>Un challenge court chaque semaine pour pratiquer regulierement.</p><ol><li>Automatiser un fichier CSV.</li><li>Refactoriser une fonction longue.</li><li>Construire une mini API.</li></ol></Card>
      </section>
      <section className="module-list">{discussions.map((item) => <Card key={item.id}><h3>{item.title}</h3><p>{item.body}</p><span className="badge">{item.theme}</span>{item.pinned && <span className="badge badge-warning">epingle</span>}</Card>)}</section>
    </div>
  );
}
