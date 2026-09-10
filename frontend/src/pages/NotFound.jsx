import { Link } from "react-router-dom";

function NotFound() {
  return (
    <main className="container" style={{ padding: "140px 0 80px" }}>
      <p>Ошибка 404</p>
      <h1>Страница не найдена</h1>
      <p>Проверьте адрес или вернитесь к списку курсов.</p>
      <Link to="/courses">Перейти к курсам</Link>
    </main>
  );
}

export default NotFound;
