import { Link } from 'react-router-dom';
import { BookOpen, Code2, Layers, Trophy } from 'lucide-react';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/ProgressBar';

export function Home() {
  const levels = [
    { title: 'Debutant complet', text: 'Aucune base requise. Tu installes Python, tu comprends les erreurs et tu codes tes premiers scripts.' },
    { title: 'Intermediaire', text: 'Tu structures tes projets, utilises les fichiers, APIs, tests, POO et bases de donnees.' },
    { title: 'Avance', text: 'Tu travailles comme un dev: architecture, typage, async, FastAPI, data, IA, securite et deploiement.' }
  ];
  const projects = ['Calculatrice', 'Bot Discord', 'API FastAPI', 'Dashboard data', 'Scraper avance', 'Portfolio complet'];
  return (
    <div className="page">
      <section className="hero">
        <div>
          <span className="eyebrow">Ecole Python en ligne</span>
          <h1>Apprends Python de zero jusqu'au niveau avance.</h1>
          <p>Une plateforme massive avec parcours, lecons, exercices, quiz, projets, corrections, badges et suivi de progression.</p>
          <div className="hero-actions"><Link className="btn btn-primary" to="/inscription">Commencer gratuitement</Link><Link className="btn btn-ghost" to="/parcours">Voir les parcours</Link></div>
        </div>
        <Card className="hero-card">
          <h3>Tableau de bord exemple</h3>
          <ProgressBar value={42} label="Progression globale" />
          <div className="stats-grid mini"><span><strong>200+</strong> lecons</span><span><strong>500+</strong> exercices</span><span><strong>50+</strong> projets</span><span><strong>100+</strong> quiz</span></div>
        </Card>
      </section>

      <section className="section-grid three">
        {levels.map((level) => <Card key={level.title}><h3>{level.title}</h3><p>{level.text}</p></Card>)}
      </section>

      <section className="section">
        <h2>Pourquoi apprendre Python ?</h2>
        <div className="section-grid four">
          <Card><BookOpen /><h3>Simple a lire</h3><p>Python permet de commencer vite sans sacrifier la puissance.</p></Card>
          <Card><Code2 /><h3>Polyvalent</h3><p>Scripts, web, data, bots, automatisation, IA et APIs.</p></Card>
          <Card><Layers /><h3>Progressif</h3><p>Chaque notion est reliee a des exercices et projets concrets.</p></Card>
          <Card><Trophy /><h3>Portfolio</h3><p>Tu termines avec des projets presentables et documentes.</p></Card>
        </div>
      </section>

      <section className="section split">
        <div><h2>Ce que tu vas apprendre</h2><p>De print() aux APIs professionnelles: variables, boucles, fonctions, collections, POO, tests, fichiers, SQL, FastAPI, pandas, automatisation, IA, Docker et CI/CD.</p></div>
        <div className="tag-cloud">{projects.map((project) => <span key={project}>{project}</span>)}</div>
      </section>

      <section className="section-grid three">
        <Card><p>"J'ai enfin compris les fonctions grace aux exemples progressifs."</p><strong>- Lina, etudiante</strong></Card>
        <Card><p>"Les projets m'ont aide a construire un portfolio credible."</p><strong>- Marc, reconversion</strong></Card>
        <Card><p>"Le dashboard montre clairement quoi faire ensuite."</p><strong>- Sarah, lyceenne</strong></Card>
      </section>

      <section className="faq">
        <h2>FAQ</h2>
        <details><summary>Faut-il savoir coder ?</summary><p>Non. Le parcours debutant part de zero.</p></details>
        <details><summary>L'editeur execute-t-il du vrai Python ?</summary><p>Par defaut, il utilise une simulation pedagogique. Le backend peut activer un runner local, mais un sandbox isole est recommande en production.</p></details>
        <details><summary>Peut-on ajouter du contenu ?</summary><p>Oui. Le panel admin et la base de donnees sont prevus pour ajouter cours, exercices, quiz, projets et ressources.</p></details>
      </section>
    </div>
  );
}
