import { useFavorites } from "./context/FavoritesContext";
export default function FavoriteButton({ id }) {
  const { ids, toggle } = useFavorites();
  const selected = ids.includes(Number(id));
  return <button type="button" className="learning-button" aria-pressed={selected}
    onClick={() => toggle(Number(id))}>{selected ? "♥ В избранном" : "♡ Отложить курс"}</button>;
}
