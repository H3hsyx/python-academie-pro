import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../api/client';
import type { Course, Lesson, Module } from '../api/types';
import { Card } from '../components/Card';

export function Cours() {
  const { courseId } = useParams();
  const [courses, setCourses] = useState<Course[]>([]);
  const [modules, setModules] = useState<Module[]>([]);
  const [lessonsByModule, setLessonsByModule] = useState<Record<number, Lesson[]>>({});
  const selectedId = Number(courseId || courses[0]?.id || 0);

  useEffect(() => { api.get<Course[]>('/courses').then(setCourses).catch(console.error); }, []);
  useEffect(() => {
    if (!selectedId) return;
    api.get<Module[]>(`/courses/${selectedId}/modules`).then(async (mods) => {
      setModules(mods);
      const pairs = await Promise.all(mods.map(async (mod) => [mod.id, await api.get<Lesson[]>(`/modules/${mod.id}/lessons`)] as const));
      setLessonsByModule(Object.fromEntries(pairs));
    }).catch(console.error);
  }, [selectedId]);

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">Cours structures</span><h1>Cours Python</h1><p>Chaque lecon suit le format objectif, explication, code, erreurs, exercice, correction, resume et quiz.</p></div></div>
      <div className="tabs">{courses.map((course) => <Link key={course.id} className={course.id === selectedId ? 'active' : ''} to={`/cours/parcours/${course.id}`}>{course.title}</Link>)}</div>
      <section className="module-list">
        {modules.map((module) => (
          <Card key={module.id}>
            <h2>{module.title}</h2><p>{module.description}</p>
            <div className="lesson-list">
              {(lessonsByModule[module.id] || []).map((lesson) => <Link key={lesson.id} to={`/cours/${lesson.id}`}><span>{lesson.order_index}. {lesson.title}</span><small>{lesson.difficulty}</small></Link>)}
            </div>
          </Card>
        ))}
      </section>
    </div>
  );
}
