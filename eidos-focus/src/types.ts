export type MissionItem = { id: string; title: string; kind: string; done: boolean };
export type Track = { id: string; title: string; done: number; total: number; color: string };
export type Application = { id: string; company: string; role: string; status: string; updated_at?: string };
export type TimerState = { duration: number; remaining: number; running: boolean; task: string; mode: "focus" };
export type Dashboard = {
  date: string;
  state_path: string;
  mission: { items: MissionItem[] };
  commitment: { outcome: string; deadline: string; focus_minutes: number; distraction: string; signed: boolean };
  metrics: { focus_minutes: number; target_minutes: number; streak: number; completed_tasks: number; project_steps: number; applications_week: number; interview_score: number; resume_percent: number };
  tracks: Track[];
  applications: Application[];
  heatmap: { date: string; minutes: number }[];
  compatibility: { learning_model: number | null; career_model: number | null; curriculum_loaded: boolean };
};
