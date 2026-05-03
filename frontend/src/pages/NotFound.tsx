import { Link } from 'react-router-dom';
import { Card } from '../components/Card';

export function NotFound() {
  return <div className="page"><Card><h1>Page introuvable</h1><p>La page demandee n'existe pas.</p><Link className="btn btn-primary" to="/">Retour accueil</Link></Card></div>;
}
