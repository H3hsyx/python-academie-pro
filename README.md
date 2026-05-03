# Python Academie Pro

Plateforme complete en francais pour apprendre Python de zero a un niveau avance.

## Objectif

Le projet fournit une vraie base de plateforme d'apprentissage, pas une page statique. Il inclut:

- Frontend React + Vite + TypeScript.
- Backend FastAPI + SQLAlchemy.
- Base SQLite par defaut, compatible PostgreSQL via `DATABASE_URL`.
- Authentification JWT avec hash de mot de passe.
- Parcours, modules, lecons, exercices, quiz, projets, ressources, challenges.
- Dashboard utilisateur avec progression, XP, niveaux, badges et recommandations.
- Profil utilisateur, favoris, communaute et panel admin.
- Mode clair/sombre responsive.
- Seed massif: 10 parcours, plus de 200 lecons, plus de 500 exercices, plus de 100 quiz, 50 projets, 30 challenges et 20 ressources.

## Comptes de demonstration

Crees automatiquement au premier demarrage si `SEED_ON_STARTUP=true`:

- Admin: `admin@python.local` / `Admin123!`
- Utilisateur: `demo@python.local` / `Demo123!`

## Installation backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API:

- Health: `http://localhost:8000/api/health`
- Docs FastAPI: `http://localhost:8000/api/docs`

## Installation frontend

```bash
cd frontend
npm install
npm run dev
```

Application:

- `http://localhost:5173`

## Docker Compose

```bash
docker compose up --build
```

Le frontend sera disponible sur `http://localhost:5173` et le backend sur `http://localhost:8000`.

## Activer l'execution Python reelle

Par defaut, `ENABLE_CODE_EXECUTION=false`. Le runner simule seulement certains `print()` pour rester prudent.

Pour une production, ne pas executer du code utilisateur directement dans le backend principal. Utiliser un sandbox separe: conteneurs jetables, limites CPU/memoire, reseau coupe, quotas, files d'attente et nettoyage automatique.

## Structure

```text
backend/app
  core/        configuration et securite
  db/          session SQLAlchemy et seed massif
  routers/     routes REST
  services/    progression, runner, slug
  models.py    modeles SQLAlchemy
  schemas.py   schemas Pydantic
frontend/src
  api/         client API et types
  components/  layout, cartes, editeur, quiz
  hooks/       auth et theme
  pages/       pages publiques, utilisateur et admin
  styles/      CSS responsive clair/sombre
```

## Principales routes API

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/courses`
- `GET /api/courses/{course_id}/modules`
- `GET /api/modules/{module_id}/lessons`
- `GET /api/lessons/{lesson_id}`
- `POST /api/lessons/{lesson_id}/complete`
- `GET /api/exercises`
- `POST /api/exercises/{exercise_id}/attempt`
- `GET /api/quizzes/{quiz_id}`
- `POST /api/quizzes/{quiz_id}/submit`
- `GET /api/projects`
- `POST /api/projects/{project_id}/submit`
- `GET /api/dashboard`
- `GET /api/profile`
- `GET /api/resources`
- `GET /api/resources/challenges/list`
- `GET /api/search?q=...`
- `GET /api/admin/stats`
- `POST /api/admin/courses`

## Evolutions recommandees

- Ajouter Alembic pour les migrations versionnees.
- Ajouter PostgreSQL en production.
- Ajouter un vrai service sandbox pour l'execution Python.
- Ajouter des tests E2E et tests API plus complets.
- Ajouter des certificats PDF et une correction manuelle des gros projets.
- Ajouter un moteur de recommandation plus avance.
