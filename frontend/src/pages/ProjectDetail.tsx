import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import type { Project } from '../api/types';
import { BadgePill } from '../components/BadgePill';
import { Card } from '../components/Card';
import { CodeBlock } from '../components/CodeBlock';

export function ProjectDetail() {
  const { projectId } = useParams();
  const [project, setProject] = useState<Project | null>(null);
  const [repositoryUrl, setRepositoryUrl] = useState('');
  const [notes, setNotes] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (projectId) api.get<Project>(`/projects/${projectId}`).then(setProject).catch(console.error);
  }, [projectId]);

  async function submit() {
    try {
      const result = await api.post<any>(`/projects/${projectId}/submit`, { repository_url: repositoryUrl, notes });
      setMessage(`Projet soumis. XP gagne: ${result.awarded_xp}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Connexion requise');
    }
  }

  if (!project) return <div className="page">Chargement...</div>;
  return (
    <div className="page">
      <div className="page-head"><div><BadgePill>{project.level}</BadgePill><h1>{project.title}</h1><p>{project.objective}</p></div></div>
      <section className="section-grid two">
        <Card><h2>Cahier des charges</h2><p>{project.specifications}</p><h3>Competences</h3><div className="tag-cloud small">{project.skills.map((skill) => <span key={skill}>{skill}</span>)}</div></Card>
        <Card><h2>Etapes detaillees</h2><ol>{project.steps?.map((step) => <li key={step}>{step}</li>)}</ol></Card>
      </section>
      <section className="section-grid two">
        <Card><h3>Code de depart</h3><CodeBlock code={project.starter_code || ''} /></Card>
        <Card><h3>Correction finale</h3><CodeBlock code={project.final_code || ''} /></Card>
      </section>
      <Card><h3>Ameliorations possibles</h3><ul>{project.improvements?.map((item) => <li key={item}>{item}</li>)}</ul><p><strong>Bonus:</strong> {project.bonus}</p></Card>
      <Card><h3>Soumettre le projet</h3><label>URL GitHub ou archive<input value={repositoryUrl} onChange={(e) => setRepositoryUrl(e.target.value)} placeholder="https://github.com/..." /></label><label>Notes<textarea value={notes} onChange={(e) => setNotes(e.target.value)} /></label><button className="btn btn-primary" onClick={submit}>Valider le projet</button>{message && <p className="notice">{message}</p>}</Card>
    </div>
  );
}
