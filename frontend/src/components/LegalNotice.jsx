import { useState } from "react";
import { Link } from "react-router-dom";

const STORAGE_KEY = "eidos-storage-notice-v1";

export default function LegalNotice() {
  const [visible, setVisible] = useState(() => localStorage.getItem(STORAGE_KEY) !== "accepted");
  if (!visible) return null;

  const accept = () => {
    localStorage.setItem(STORAGE_KEY, "accepted");
    setVisible(false);
  };

  return (
    <aside className="legal-notice" aria-label="Уведомление о данных браузера">
      <div>
        <strong>Данные браузера</strong>
        <p>Eidos использует localStorage для входа, темы, избранного и поиска. Рекламных cookie нет.</p>
        <Link to="/legal/cookies">Подробнее</Link>
      </div>
      <button type="button" onClick={accept}>Понятно</button>
    </aside>
  );
}
