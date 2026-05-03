import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import type { Exercise } from '../api/types';
import { BadgePill } from '../components/BadgePill';
import { Card } from '../components/Card';

export function Exercices() {
  const [items, setItems] = useState<Exercise[]>([]);
  const [query, setQuery] = useState({ level: '', difficulty: '', q: '' });

  useEffect(() => {
    const params = new URLSearchParams();
    if (query.level) params.set('level', query.level);
    if (query.difficulty) params.set('difficulty', query.difficulty);
    if (query.q) params.set('q', query.q);
    api.get<Exercise[]>(`/exercises?${params.toString()}`).then(setItems).catch(console.error);
  }, [query]);

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">500+ exercices prevus</span><h1>Exercices Python</h1><p>Completer du code, corriger une erreur, ecrire une fonction, lire du code, challenges et projets guides.</p></div></div>
      <div className="filters">
        <input placeholder="Rechercher" value={query.q} onChange={(e) => setQuery({ ...query, q: e.target.value })} />
        <select value={query.level} onChange={(e) => setQuery({ ...query, level: e.target.value })}><option value="">Tous niveaux</option><option>Debutant</option><option>Intermediaire</option><option>Avance</option></select>
        <select value={query.difficulty} onChange={(e) => setQuery({ ...query, difficulty: e.target.value })}><option value="">Toutes difficultes</option><option>facile</option><option>moyen</option><option>difficile</option></select>
      </div>
      <section className="section-grid three">
        {items.map((item) => <Card key={item.id}><BadgePill>{item.level}</BadgePill><h3>{item.title}</h3><p>{item.description}</p><p><strong>{item.exercise_type}</strong> - {item.duration_minutes} min</p><BadgePill tone={item.difficulty === 'difficile' ? 'danger' : item.difficulty === 'moyen' ? 'warning' : 'success'}>{item.difficulty}</BadgePill><Link className="btn btn-primary" to={`/exercices/${item.id}`}>Resoudre</Link></Card>)}
      </section>
    </div>
  );
}
