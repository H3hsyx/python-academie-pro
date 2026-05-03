import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { BadgePill } from '../components/BadgePill';
import { Card } from '../components/Card';

export function Resources() {
  const [resources, setResources] = useState<any[]>([]);
  const [challenges, setChallenges] = useState<any[]>([]);
  useEffect(() => {
    api.get<any[]>('/resources').then(setResources).catch(console.error);
    api.get<any[]>('/resources/challenges/list').then(setChallenges).catch(console.error);
  }, []);

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">Fiches, guides, challenges</span><h1>Ressources</h1><p>Cheatsheets Python, glossaire, erreurs frequentes, raccourcis, docs et conseils portfolio.</p></div></div>
      <section className="section-grid three">{resources.map((item) => <Card key={item.id}><BadgePill>{item.kind}</BadgePill><h3>{item.title}</h3><p>{item.content.slice(0, 180)}...</p><div className="tag-cloud small">{item.tags.map((tag: string) => <span key={tag}>{tag}</span>)}</div></Card>)}</section>
      <h2>Challenges</h2>
      <section className="section-grid three">{challenges.slice(0, 12).map((item) => <Card key={item.id}><BadgePill>{item.level}</BadgePill><h3>{item.title}</h3><p>{item.description}</p><p>{item.duration_minutes} min - {item.points} points</p></Card>)}</section>
    </div>
  );
}
