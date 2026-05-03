import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import type { Course } from '../api/types';
import { BadgePill } from '../components/BadgePill';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/ProgressBar';

export function Parcours() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [level, setLevel] = useState('');

  useEffect(() => {
    api.get<Course[]>(`/courses${level ? `?level=${level}` : ''}`).then(setCourses).catch(console.error);
  }, [level]);

  return (
    <div className="page">
      <div className="page-head"><div><span className="eyebrow">10 parcours complets</span><h1>Parcours Python</h1><p>Choisis une progression adaptee a ton niveau et a ton objectif.</p></div></div>
      <div className="filters"><button onClick={() => setLevel('')}>Tous</button><button onClick={() => setLevel('Debutant')}>Debutant</button><button onClick={() => setLevel('Intermediaire')}>Intermediaire</button><button onClick={() => setLevel('Avance')}>Avance</button></div>
      <section className="section-grid three">
        {courses.map((course, index) => (
          <Card key={course.id}>
            <BadgePill tone={course.level === 'Avance' ? 'warning' : 'neutral'}>{course.level}</BadgePill>
            <h3>{course.title}</h3>
            <p>{course.description}</p>
            <ProgressBar value={(index * 13) % 100} label="Progression" />
            <ul className="compact-list">{course.objectives.slice(0, 3).map((item) => <li key={item}>{item}</li>)}</ul>
            <p><strong>Duree:</strong> {course.estimated_duration}</p>
            <Link className="btn btn-primary" to={`/parcours/${course.id}`}>Ouvrir</Link>
          </Card>
        ))}
      </section>
    </div>
  );
}
