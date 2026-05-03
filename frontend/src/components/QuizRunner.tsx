import { useState } from 'react';
import { api } from '../api/client';
import type { Quiz } from '../api/types';

export function QuizRunner({ quiz }: { quiz: Quiz }) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  async function submit() {
    try {
      setError('');
      const data = await api.post(`/quizzes/${quiz.id}/submit`, { answers });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur');
    }
  }

  return (
    <section className="quiz-card">
      <h3>{quiz.title}</h3>
      <p>{quiz.description}</p>
      {quiz.questions.map((question) => (
        <fieldset key={question.id} className="quiz-question">
          <legend>{question.question}</legend>
          {question.options.map((option) => (
            <label key={option}>
              <input type="radio" name={`q-${question.id}`} value={option} onChange={(e) => setAnswers({ ...answers, [String(question.id)]: e.target.value })} />
              {option}
            </label>
          ))}
        </fieldset>
      ))}
      <button className="btn btn-primary" onClick={submit}>Valider le quiz</button>
      {error && <p className="error">{error}</p>}
      {result && <pre className="terminal small">{JSON.stringify(result, null, 2)}</pre>}
    </section>
  );
}
