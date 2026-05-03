export type User = {
  id: number;
  username: string;
  email: string;
  role: string;
  level: string;
  xp: number;
  streak_days: number;
  avatar_url?: string | null;
  created_at: string;
  last_login?: string | null;
};

export type Course = {
  id: number;
  slug: string;
  title: string;
  description: string;
  level: string;
  track_type: string;
  order_index: number;
  estimated_duration: string;
  objectives: string[];
  final_projects: string[];
};

export type Module = {
  id: number;
  course_id: number;
  title: string;
  description: string;
  level: string;
  order_index: number;
  estimated_duration: string;
};

export type Lesson = {
  id: number;
  module_id: number;
  slug: string;
  title: string;
  order_index: number;
  difficulty: string;
  summary: string;
  content?: string;
  code_examples?: { title: string; language: string; code: string; explanation: string }[];
  objectives?: string[];
  common_errors?: string[];
  tips?: string[];
  mini_exercise?: Record<string, unknown>;
};

export type Exercise = {
  id: number;
  lesson_id?: number | null;
  slug: string;
  title: string;
  description: string;
  starter_code: string;
  expected_output: string;
  solution: string;
  optimized_solution: string;
  explanation: string;
  difficulty: string;
  level: string;
  theme: string;
  duration_minutes: number;
  exercise_type: string;
  hints: string[];
  tests: Record<string, unknown>[];
  points: number;
};

export type Project = {
  id: number;
  slug: string;
  title: string;
  description: string;
  level: string;
  category: string;
  estimated_duration: string;
  objective: string;
  skills: string[];
  difficulty: string;
  specifications?: string;
  steps?: string[];
  starter_code?: string;
  hints?: string[];
  final_code?: string;
  improvements?: string[];
  bonus?: string;
};

export type Quiz = {
  id: number;
  title: string;
  description: string;
  difficulty: string;
  time_limit_minutes: number;
  questions: { id: number; question: string; question_type: string; options: string[]; points: number }[];
};

export type Badge = {
  id: number;
  code: string;
  title: string;
  description: string;
  icon: string;
  xp_required: number;
  rule_type: string;
  rule_value: number;
};

export type Dashboard = {
  user: User;
  global_completion: number;
  lessons_done: number;
  exercises_passed: number;
  projects_done: number;
  quizzes_passed: number;
  badges: { id: number; awarded_at: string; badge: Badge }[];
  recommendations: Lesson[];
  last_lesson?: Lesson | null;
  weekly_goal: { target_minutes: number; done_minutes: number; message: string };
  xp_to_next_level: number;
};
