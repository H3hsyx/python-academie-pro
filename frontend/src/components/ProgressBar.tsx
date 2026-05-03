export function ProgressBar({ value, label }: { value: number; label?: string }) {
  const safe = Math.max(0, Math.min(100, Math.round(value || 0)));
  return (
    <div className="progress-wrap" aria-label={label || `Progression ${safe}%`}>
      <div className="progress-meta"><span>{label || 'Progression'}</span><strong>{safe}%</strong></div>
      <div className="progress"><span style={{ width: `${safe}%` }} /></div>
    </div>
  );
}
