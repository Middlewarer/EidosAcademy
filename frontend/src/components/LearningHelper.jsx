import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

const answers = [
  { question: "Как начать учиться?", words: /нач|учить/, text: "Выберите курс, посмотрите программу и нажмите «Начать обучение». Для сохранения прогресса понадобится войти в аккаунт.", to: "/courses", link: "Выбрать курс" },
  { question: "Где мой прогресс?", words: /прогресс|продол|профиль/, text: "Ваши начатые курсы находятся в профиле. Открытая тема и пройденная тема — разные статусы: отмечайте материал пройденным после изучения.", to: "/profile", link: "Открыть профиль" },
  { question: "Как отложить курс?", words: /избран|отлож|сохран/, text: "Нажмите «Отложить курс» на карточке. Избранное сохраняется в этом браузере, даже без входа. На другом устройстве список будет отдельным.", to: "/favorites", link: "Моё избранное" },
  { question: "Нашёл ошибку", words: /ошиб|баг|проблем|отзыв/, text: "Опишите, на какой странице возникла проблема и что вы делали. Отправьте сообщение через обратную связь.", to: "/feedback", link: "Сообщить о проблеме" },
];
export default function LearningHelper() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const log = useRef(null);
  const input = useRef(null);
  const trigger = useRef(null);
  useEffect(() => { if (open) input.current?.focus(); }, [open]);
  useEffect(() => { if (log.current) log.current.scrollTop = log.current.scrollHeight; }, [messages]);
  function ask(question) {
    if (!question.trim()) return;
    const answer = answers.find((item) => item.question === question)
      || answers.find((item) => item.words.test(question.toLowerCase()));
    setMessages((current) => [...current.slice(-18), { question, answer: answer || { text: "Я справочный бот и отвечаю на вопросы о платформе. Выберите подсказку ниже или напишите через обратную связь.", to: "/feedback", link: "Обратная связь" } }]);
    setQuery("");
  }
  function close() { setOpen(false); trigger.current?.focus(); }
  return <aside className="learning-helper" aria-label="Помощь по платформе">
    {open && <section id="learning-helper-panel" className="learning-helper__panel" onKeyDown={(event) => { if (event.key === "Escape") close(); }}>
      <div className="learning-toolbar"><strong>Помощник Eidos</strong><button className="learning-button" onClick={close} aria-label="Закрыть помощника">✕</button></div>
      <p>Справочный бот по платформе. Выберите вопрос или напишите свой.</p>
      <div className="learning-helper__log" ref={log} role="log" aria-live="polite">
        {messages.map((message, index) => <div key={index} className="learning-helper__message">
          <strong>{message.question}</strong><p>{message.answer.text}</p><Link onClick={close} to={message.answer.to}>{message.answer.link} →</Link>
        </div>)}
      </div>
      <div className="learning-helper__suggestions">{answers.map((item) => <button className="learning-button" key={item.question} onClick={() => ask(item.question)}>{item.question}</button>)}</div>
      <form onSubmit={(event) => { event.preventDefault(); ask(query); }}>
        <label htmlFor="helper-query">Ваш вопрос</label>
        <div className="learning-actions"><input ref={input} id="helper-query" className="learning-input" maxLength={300} value={query} onChange={(event) => setQuery(event.target.value)} /><button className="learning-button" disabled={!query.trim()}>Отправить</button></div>
      </form>
    </section>}
    <button ref={trigger} className="learning-button learning-button--primary" aria-expanded={open} aria-controls="learning-helper-panel" onClick={() => setOpen(!open)}> {open ? "Скрыть помощника" : "Помощь с обучением"}</button>
  </aside>;
}
