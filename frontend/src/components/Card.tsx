export function Card({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <article className={`card ${className}`}>{children}</article>;
}
