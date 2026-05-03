import Editor from '@monaco-editor/react';
import { useState } from 'react';
import { Play, RotateCcw } from 'lucide-react';
import { api } from '../api/client';

export function CodeEditor({ starterCode, exerciseId }: { starterCode: string; exerciseId?: number }) {
  const [code, setCode] = useState(starterCode || "print('Python')");
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  async function run() {
    setLoading(true);
    try {
      const result = exerciseId
        ? await api.post<{ stdout: string; stderr: string; passed: boolean; expected_output: string; explanation: string }>(`/exercises/${exerciseId}/attempt`, { submitted_code: code })
        : await api.post<{ stdout: string; stderr: string; mode: string }>('/exercises/run', { submitted_code: code });
      setOutput(JSON.stringify(result, null, 2));
    } catch (error) {
      setOutput(error instanceof Error ? error.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="editor-card">
      <div className="editor-toolbar">
        <strong>Editeur Python</strong>
        <div>
          <button className="btn btn-ghost" onClick={() => setCode(starterCode)}><RotateCcw size={16} /> Recommencer</button>
          <button className="btn btn-primary" onClick={run} disabled={loading}><Play size={16} /> {loading ? 'Test...' : 'Lancer'}</button>
        </div>
      </div>
      <Editor height="360px" defaultLanguage="python" value={code} onChange={(value) => setCode(value || '')} theme={document.documentElement.dataset.theme === 'dark' ? 'vs-dark' : 'light'} options={{ minimap: { enabled: false }, fontSize: 14, wordWrap: 'on' }} />
      <div className="terminal" aria-live="polite"><strong>Sortie</strong><pre>{output || 'Aucun resultat pour le moment.'}</pre></div>
    </section>
  );
}
