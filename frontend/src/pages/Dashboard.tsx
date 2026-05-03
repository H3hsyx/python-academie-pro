import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import type { Dashboard as DashboardType } from '../api/types';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/ProgressBar';

export function Dashboard() {
  const [data, setData] = useState<DashboardType | null>(null);
  useEffect(() => { api.get<DashboardType>('/dashboard').then(setData).catch(console.error); }, []);
  if (!data) return <div className="page">Chargement du dashboard...</div>;
  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">Bienvenue {data.user.username}</span><h1>Tableau de bord</h1><p>Niveau actuel: {data.user.level}. XP: {data.user.xp}. Prochain niveau dans {data.xp_to_next_level} XP.</p></div></div>
      <Card><ProgressBar value={data.global_completion} label="Completion globale" /></Card>
      <section className="stats-grid">
        <Card><strong>{data.lessons_done}</strong><span>Lecons terminees</span></Card>
        <Card><strong>{data.exercises_passed}</strong><span>Exercices reussis</span></Card>
        <Card><strong>{data.projects_done}</strong><span>Projets realises</span></Card>
        <Card><strong>{data.quizzes_passed}</strong><span>Quiz reussis</span></Card>
      </section>
      <section className="section-grid two">
        <Card><h2>Derniere lecon</h2>{data.last_lesson ? <Link to={`/cours/${data.last_lesson.id}`}>{data.last_lesson.title}</Link> : <p>Commence une premiere lecon.</p>}<p>{data.weekly_goal.message}</p></Card>
        <Card><h2>Badges gagnes</h2><div className="tag-cloud small">{data.badges.map((item) => <span key={item.id}>{item.badge.title}</span>)}</div></Card>
      </section>
      <Card><h2>Recommandations</h2><div className="lesson-list">{data.recommendations.map((lesson) => <Link key={lesson.id} to={`/cours/${lesson.id}`}>{lesson.title}<small>{lesson.difficulty}</small></Link>)}</div></Card>
    </div>
  );
}
