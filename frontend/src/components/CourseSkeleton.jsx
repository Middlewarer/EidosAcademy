export default function CourseSkeleton() {
  return <div className="animate-pulse rounded-3xl border border-[var(--line)] bg-[var(--white)] p-5 sm:p-6" role="status" aria-label="Загрузка курса">
    <div className="aspect-video rounded-2xl bg-slate-200 dark:bg-slate-700" />
    <div className="mt-5 h-5 w-3/4 rounded-full bg-slate-200 dark:bg-slate-700" />
    <div className="mt-4 h-3 w-full rounded-full bg-slate-200 dark:bg-slate-700" />
    <div className="mt-2 h-3 w-2/3 rounded-full bg-slate-200 dark:bg-slate-700" />
    <span className="sr-only">Загрузка…</span>
  </div>;
}
