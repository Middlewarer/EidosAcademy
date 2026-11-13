import type { Dashboard, MissionItem, TimerState } from "./types";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, { ...options, headers: { "Content-Type": "application/json", ...(options?.headers || {}) } });
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).error || `Ошибка ${response.status}`);
  return response.json();
}

export const api = {
  dashboard: () => request<Dashboard>("/api/dashboard"),
  timer: () => request<TimerState>("/api/timer"),
  timerAction: (action: "start" | "pause" | "reset" | "complete", task = "") => request<TimerState>("/api/timer", { method: "POST", body: JSON.stringify({ action, task }) }),
  mission: (items: MissionItem[]) => request<Dashboard>("/api/mission", { method: "PUT", body: JSON.stringify({ items }) }),
  commitment: (value: Dashboard["commitment"]) => request<Dashboard>("/api/commitment", { method: "PUT", body: JSON.stringify(value) }),
  session: (task: string, elapsed_seconds: number, completed: boolean) => request<Dashboard>("/api/focus-session", { method: "POST", body: JSON.stringify({ task, elapsed_seconds, completed }) }),
  application: (company: string, role: string) => request<Dashboard>("/api/applications", { method: "POST", body: JSON.stringify({ company, role }) })
};
