import { createContext, useContext, useEffect, useState } from "react";
import toast from "react-hot-toast";

const FavoritesContext = createContext(null);
const KEY = "eidos:favorites";
function readFavorites() {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) || "[]");
    return Array.isArray(saved) ? [...new Set(saved.filter((id) => Number.isSafeInteger(id) && id > 0))] : [];
  } catch { return []; }
}
export function FavoritesProvider({ children }) {
  const [ids, setIds] = useState(readFavorites);
  useEffect(() => {
    const sync = (event) => { if (event.key === KEY || event.key === null) setIds(readFavorites()); };
    window.addEventListener("storage", sync);
    return () => window.removeEventListener("storage", sync);
  }, []);
  function save(next) {
    try {
      localStorage.setItem(KEY, JSON.stringify(next));
      setIds(next);
    } catch { toast.error("Браузер не разрешил сохранить избранное."); }
  }
  function toggle(id) {
    save(ids.includes(id) ? ids.filter((value) => value !== id) : [...ids, id]);
  }
  return <FavoritesContext.Provider value={{ ids, toggle, clear: () => save([]) }}>{children}</FavoritesContext.Provider>;
}
// eslint-disable-next-line react-refresh/only-export-components
export function useFavorites() { return useContext(FavoritesContext); }
