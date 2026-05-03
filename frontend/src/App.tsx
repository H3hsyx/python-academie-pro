import { Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Admin } from './pages/Admin';
import { Community } from './pages/Community';
import { Cours } from './pages/Cours';
import { Dashboard } from './pages/Dashboard';
import { ExercisePage } from './pages/ExercisePage';
import { Exercices } from './pages/Exercices';
import { Home } from './pages/Home';
import { LessonPage } from './pages/LessonPage';
import { Login } from './pages/Login';
import { NotFound } from './pages/NotFound';
import { Parcours } from './pages/Parcours';
import { Profile } from './pages/Profile';
import { ProjectDetail } from './pages/ProjectDetail';
import { Projects } from './pages/Projects';
import { Register } from './pages/Register';
import { Resources } from './pages/Resources';
import { SearchPage } from './pages/SearchPage';

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/parcours" element={<Parcours />} />
        <Route path="/parcours/:courseId" element={<Cours />} />
        <Route path="/cours" element={<Cours />} />
        <Route path="/cours/parcours/:courseId" element={<Cours />} />
        <Route path="/cours/:lessonId" element={<LessonPage />} />
        <Route path="/exercices" element={<Exercices />} />
        <Route path="/exercices/:exerciseId" element={<ExercisePage />} />
        <Route path="/projets" element={<Projects />} />
        <Route path="/projets/:projectId" element={<ProjectDetail />} />
        <Route path="/communaute" element={<Community />} />
        <Route path="/ressources" element={<Resources />} />
        <Route path="/recherche" element={<SearchPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profil" element={<Profile />} />
        </Route>
        <Route element={<ProtectedRoute adminOnly />}>
          <Route path="/admin" element={<Admin />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Route>
      <Route path="/connexion" element={<Login />} />
      <Route path="/inscription" element={<Register />} />
    </Routes>
  );
}
