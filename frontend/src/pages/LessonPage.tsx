import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../api/client';
import type { Lesson } from '../api/types';
import { BadgePill } from '../components/BadgePill';
import { Card } from '../components/Card';
import { CodeBlock } from '../components/CodeBlock';

export function LessonPage() {
  const { lessonId } = useParams();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (lessonId) api.get<Lesson>(`/lessons/${lessonId}`).then(setLesson).catch(console.error);
  }, [lessonId]);

  async function complete() {
    try {
      const result = await api.post<{ message: string; xp: number; level: string }>(`/lessons/${lessonId}/complete`);
      setMessage(`${result.message}. XP total: ${result.xp}. Niveau: ${result.level}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Connexion requise');
    }
  }

  if (!lesson) return <div className="page">Chargement...</div>;
  return (
    <div className="page lesson-page">
      <div className="page-head"><div><BadgePill>{lesson.difficulty}</BadgePill><h1>{lesson.title}</h1><p>{lesson.summary}</p></div><button className="btn btn-primary" onClick={complete}>Marquer comme termine</button></div>
      {message && <p className="notice">{message}</p>}
      <Card>
        <h2>Objectifs</h2>
        <ul className="compact-list">{lesson.objectives?.map((item) => <li key={item}>{item}</li>)}</ul>
      </Card>
      <Card>
        <div className="lesson-content">{lesson.content?.split('\n').map((line, i) => line.startsWith('#') ? <h2 key={i}>{line.replace(/^#+\s*/, '')}</h2> : line.startsWith('```') ? null : <p key={i}>{line}</p>)}</div>
      </Card>
      <section className="section-grid two">
        {lesson.code_examples?.map((example) => <Card key={example.title}><h3>{example.title}</h3><CodeBlock code={example.code} /><p>{example.explanation}</p></Card>)}
      </section>
      <section className="section-grid two">
        <Card><h3>Erreurs frequentes</h3><ul>{lesson.common_errors?.map((item) => <li key={item}>{item}</li>)}</ul></Card>
        <Card><h3>Astuces</h3><ul>{lesson.tips?.map((item) => <li key={item}>{item}</li>)}</ul></Card>
      </section>
      <Card><h3>Mini-exercice</h3><p>{String(lesson.mini_exercise?.prompt || '')}</p><p><strong>Correction attendue:</strong> {String(lesson.mini_exercise?.expected || '')}</p></Card>
      <div className="next-actions"><Link className="btn btn-ghost" to="/exercices">Faire des exercices</Link><button className="btn btn-primary" onClick={complete}>Lecon suivante</button></div>
    </div>
  );
}
