import { useState } from "react";
import { Link } from "react-router-dom";
const steps = [
  { title: "Найдите своё направление", text: "Изучите программу курса в быстром просмотре. Сохраните интересные курсы в избранное, чтобы спокойно выбрать, с чего начать.", to: "/courses", action: "Посмотреть курсы" },
  { title: "Начните с одной темы", text: "Откройте курс и начните обучение. После входа платформа сохранит, где вы остановились, — возвращаться к материалам будет проще.", to: "/favorites", action: "Перейти к избранному" },
  { title: "Закрепляйте изученное", text: "Попробуйте пример из урока самостоятельно. Затем отметьте тему пройденной и проверьте свой прогресс в профиле.", to: "/profile", action: "Мои курсы и прогресс" },
];
export default function LearningPath() {
  const [index, setIndex] = useState(0);
  const step = steps[index];
  return <section id="learning" className="container learning-path" aria-label="Как организовать обучение" aria-roledescription="карусель">
    <span>Ваш следующий шаг · {index + 1} / {steps.length}</span>
    <div className="learning-path__content" aria-live="polite" aria-atomic="true">
      <h2 className="learning-path__heading">{step.title}</h2><p>{step.text}</p>
      <Link className="learning-button learning-button--primary" to={step.to}>{step.action} →</Link>
    </div>
    <div className="learning-path__controls d-flex flex-wrap align-items-center gap-3">
      <button className="learning-button" onClick={() => setIndex((index + steps.length - 1) % steps.length)} aria-label="Предыдущий совет">←</button>
      {steps.map((step, position) => <button key={step.title} className="learning-path__dot" aria-label={step.title} aria-current={position === index ? "true" : undefined} onClick={() => setIndex(position)} />)}
      <button className="learning-button" onClick={() => setIndex((index + 1) % steps.length)} aria-label="Следующий совет">→</button>
    </div>
  </section>;
}
