import { Link } from "react-router-dom";

function NotFound() {
  return (
    <main className="container not-found-page">
      <span>Ошибка 404</span>
      <h1>Страница не найдена</h1>
      <p>Проверьте адрес или вернитесь к списку курсов.</p>
      <Link to="/courses" className="learning-button learning-button--primary">Перейти к курсам</Link>
    </main>
  );
}

export default NotFound;
