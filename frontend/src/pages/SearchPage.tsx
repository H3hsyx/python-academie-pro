import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { api } from '../api/client';
import { Card } from '../components/Card';

export function SearchPage() {
  const [params] = useSearchParams();
  const q = params.get('q') || '';
  const [results, setResults] = useState<any[]>([]);

  useEffect(() => {
    if (q.length >= 2) api.get<any[]>(`/search?q=${encodeURIComponent(q)}`).then(setResults).catch(console.error);
  }, [q]);

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">Recherche globale</span><h1>Resultats pour "{q}"</h1><p>Cours, exercices, projets, concepts, erreurs et ressources.</p></div></div>
      <section className="module-list">
        {results.map((item) => <Card key={`${item.entity_type}-${item.entity_id}`}><span className="badge">{item.entity_type}</span><h3>{item.title}</h3><p>{item.description}</p><Link className="btn btn-ghost" to={item.url}>Ouvrir</Link></Card>)}
      </section>
    </div>
  );
}
