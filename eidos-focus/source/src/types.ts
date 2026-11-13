export type MissionItem = { id: string; title: string; kind: string; done: boolean };
export type Track = { id: string; title: string; done: number; total: number; color: string };
export type LearningTopic = { id: string; number: number; title: string; done: number; total: number; has_exam: boolean };
export type LearningTrack = Track & { number: number; goal: string; topics: LearningTopic[] };
export type LearningIndex = { loaded: boolean; tracks: LearningTrack[] };
export type TopicTask = { id: string; title: string; label: string; kind: string; statement: string; deliverable: string; example: string; difficulty: string; minutes: number; artifact: string; external_url: string; done: boolean };
export type TopicDetail = {
  loaded: boolean;
  track: { id: string; title: string; goal: string; color: string };
  topic: { id: string; number: number; title: string; theory: string; pitfall: string; mastery: string; practice_links: string[]; tasks: TopicTask[]; mentor_prompt: string; exam: null | { title: string; description: string; minutes: number; exam_prompt: string } };
};
export type Application = { id: string; company: string; role: string; status: string; updated_at?: string };
export type PomodoroSettings = { focus_minutes: number; break_minutes: number; ambient_sound: "none" | "rain" | "fire" | "ocean"; ambient_volume: number; auto_start_break: boolean };
export type TimerState = { duration: number; remaining: number; running: boolean; task: string; mode: "focus" | "break"; focus_minutes?: number; break_minutes?: number };
export type Dashboard = {
  date: string;
  state_path: string;
  mission: { items: MissionItem[] };
  metrics: { focus_minutes: number; target_minutes: number; streak: number; completed_tasks: number; project_steps: number; applications_week: number; interview_score: number; resume_percent: number };
  pace: { status: "behind" | "on_track" | "ahead"; actual_tasks: number; expected_tasks: number; total_tasks: number; gap_tasks: number; actual_percent: number; expected_percent: number; days_remaining: number; target_date: string; tasks_per_day_needed: number };
  pomodoro: PomodoroSettings;
  tracks: Track[];
  applications: Application[];
  heatmap: { date: string; minutes: number }[];
  compatibility: { learning_model: number | null; career_model: number | null; curriculum_loaded: boolean };
};
