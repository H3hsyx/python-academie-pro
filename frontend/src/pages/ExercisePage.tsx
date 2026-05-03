import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import type { Exercise } from '../api/types';
import { BadgePill } from '../components/BadgePill';
import { Card } from '../components/Card';
import { CodeBlock } from '../components/CodeBlock';
import { CodeEditor } from '../components/CodeEditor';

export function ExercisePage() {
  const { exerciseId } = useParams();
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [showSolution, setShowSolution] = useState(false);

  useEffect(() => {
    if (exerciseId) api.get<Exercise>(`/exercises/${exerciseId}`).then(setExercise).catch(console.error);
  }, [exerciseId]);

  if (!exercise) return <div className="page">Chargement...</div>;
  return (
    <div className="page">
      <div className="page-head"><div><BadgePill>{exercise.level}</BadgePill><h1>{exercise.title}</h1><p>{exercise.description}</p></div></div>
      <section className="section-grid two">
        <Card><h2>Enonce</h2><p><strong>Type:</strong> {exercise.exercise_type}</p><p><strong>Difficulte:</strong> {exercise.difficulty}</p><p><strong>Sortie attendue:</strong></p><CodeBlock code={exercise.expected_output} /><h3>Indices progressifs</h3><ol>{exercise.hints.map((hint) => <li key={hint}>{hint}</li>)}</ol></Card>
        <CodeEditor starterCode={exercise.starter_code} exerciseId={exercise.id} />
      </section>
      <Card><button className="btn btn-ghost" onClick={() => setShowSolution(!showSolution)}>{showSolution ? 'Masquer' : 'Voir'} la correction detaillee</button>{showSolution && <div><h3>Correction simple</h3><CodeBlock code={exercise.solution} /><h3>Correction optimisee</h3><CodeBlock code={exercise.optimized_solution} /><p>{exercise.explanation}</p></div>}</Card>
    </div>
  );
}
