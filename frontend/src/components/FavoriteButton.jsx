import { useFavorites } from "./context/FavoritesContext";
export default function FavoriteButton({ id }) {
  const { ids, toggle } = useFavorites();
  const selected = ids.includes(Number(id));
  return <button type="button" className={`rounded-xl border px-4 py-2.5 text-sm font-bold transition hover:-translate-y-0.5 ${selected
    ? "border-rose-300 bg-rose-50 text-rose-700 dark:border-rose-900 dark:bg-rose-950/30 dark:text-rose-300"
    : "border-[var(--line)] bg-[var(--paper)] text-[var(--ink)] hover:border-[var(--blue)]"}`} aria-pressed={selected}
    onClick={() => toggle(Number(id))}>{selected ? "♥ В избранном" : "♡ Отложить курс"}</button>;
}
