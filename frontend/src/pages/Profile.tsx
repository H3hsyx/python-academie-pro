import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Badge, User } from '../api/types';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/ProgressBar';

export function Profile() {
  const [user, setUser] = useState<User | null>(null);
  const [badges, setBadges] = useState<{ badge: Badge; awarded_at: string }[]>([]);
  const [progress, setProgress] = useState<any[]>([]);

  useEffect(() => {
    api.get<User>('/profile').then(setUser).catch(console.error);
    api.get<any[]>('/profile/badges').then(setBadges).catch(console.error);
    api.get<any[]>('/profile/progress').then(setProgress).catch(console.error);
  }, []);

  if (!user) return <div className="page">Chargement...</div>;
  const percent = Math.min(100, Math.round((user.xp / 5000) * 100));
  return (
    <div className="page">
      <div className="profile-hero"><div className="avatar">{user.username.slice(0, 2).toUpperCase()}</div><div><h1>{user.username}</h1><p>{user.email}</p><p>Niveau: <strong>{user.level}</strong></p></div></div>
      <Card><ProgressBar value={percent} label="Progression vers Python Master" /></Card>
      <section className="section-grid three">
        <Card><strong>{user.xp}</strong><span>XP gagnes</span></Card>
        <Card><strong>{badges.length}</strong><span>Badges</span></Card>
        <Card><strong>{progress.length}</strong><span>Elements suivis</span></Card>
      </section>
      <Card><h2>Badges et certificats</h2><div className="tag-cloud small">{badges.map((item) => <span key={item.badge.id}>{item.badge.title}</span>)}</div></Card>
    </div>
  );
}
