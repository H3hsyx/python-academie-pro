import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import type { Project } from '../api/types';
import { BadgePill } from '../components/BadgePill';
import { Card } from '../components/Card';

export function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [level, setLevel] = useState('');

  useEffect(() => {
    api.get<Project[]>(`/projects${level ? `?level=${level}` : ''}`).then(setProjects).catch(console.error);
  }, [level]);

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">50 projets concrets</span><h1>Projets Python</h1><p>Chaque projet inclut objectif, cahier des charges, etapes, indices, correction et ameliorations.</p></div></div>
      <div className="filters"><button onClick={() => setLevel('')}>Tous</button><button onClick={() => setLevel('Debutant')}>Debutant</button><button onClick={() => setLevel('Intermediaire')}>Intermediaire</button><button onClick={() => setLevel('Avance')}>Avance</button></div>
      <section className="section-grid three">
        {projects.map((project) => <Card key={project.id}><BadgePill>{project.level}</BadgePill><h3>{project.title}</h3><p>{project.description}</p><p><strong>{project.category}</strong> - {project.estimated_duration}</p><div className="tag-cloud small">{project.skills.slice(0, 3).map((skill) => <span key={skill}>{skill}</span>)}</div><Link className="btn btn-primary" to={`/projets/${project.id}`}>Voir le projet</Link></Card>)}
      </section>
    </div>
  );
}
