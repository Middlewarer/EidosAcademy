import { useEffect, useRef, useState } from "react";
import { apiRequest } from "../components/api/apiRequest";
import { useAuth } from "../components/context/AuthContext";
import "../styles/FeedbackPage.css";

const kinds = [
  { value: "review", icon: "♥", title: "Отзыв", hint: "Что вам понравилось?" },
  { value: "idea", icon: "✦", title: "Пожелание", hint: "Чего не хватает?" },
  { value: "bug", icon: "⚑", title: "Ошибка", hint: "Что работает не так?" },
];

const statusClass = {
  new: "neutral",
  seen: "neutral",
  planned: "planned",
  resolved: "resolved",
  rejected: "neutral",
};

function FeedbackEntry({ entry }) {
  const [expanded, setExpanded] = useState(false);
  const [overflowing, setOverflowing] = useState(false);
  const textRef = useRef(null);
  useEffect(() => {
    const element = textRef.current;
    if (!element || expanded) return;
    const measure = () => setOverflowing(element.scrollHeight > element.clientHeight + 1);
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    return () => observer.disconnect();
  }, [expanded, entry.message]);
  const author = entry.author || "Аноним";
  return (
    <article className="community-message">
      <div className={`community-avatar community-avatar--${entry.kind}`} aria-hidden="true">
        {author.charAt(0).toUpperCase()}
      </div>
      <div className="community-message-content">
        <div className="community-message-heading">
          <div className="community-identity">
            <strong>{author}</strong>
            <time dateTime={entry.created_at}>{new Intl.DateTimeFormat("ru-RU", {
              day: "numeric", month: "short", year: "numeric",
            }).format(new Date(entry.created_at))}</time>
          </div>
          <span className={`community-status community-status--${statusClass[entry.status] || "neutral"}`}>
            <span aria-hidden="true" />{entry.status_label}
          </span>
        </div>
        <span className="community-type">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            {entry.kind === "review" ? <path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9H13a8.5 8.5 0 0 1 8 8v.5Z" />
              : entry.kind === "idea" ? <><path d="M9 18h6m-5 3h4M8 14a6 6 0 1 1 8 0c-1 1-1 2-1 2H9s0-1-1-2Z" /></>
              : <><circle cx="12" cy="12" r="9" /><path d="M12 7v6m0 4h.01" /></>}
          </svg>
          {entry.kind_label}
        </span>
        <p ref={textRef} id={`message-${entry.id}`} className={`community-text ${expanded ? "is-expanded" : ""}`}>{entry.message}</p>
        {(overflowing || expanded) && (
          <button type="button" className="community-expand" aria-expanded={expanded}
            aria-controls={`message-${entry.id}`} onClick={() => setExpanded(!expanded)}>
            {expanded ? "Свернуть сообщение ↑" : "Показать полностью ↓"}
          </button>
        )}
      </div>
    </article>
  );
}

function getErrorMessage(data) {
  if (typeof data?.detail === "string") return data.detail;
  const first = Object.values(data || {})[0];
  if (Array.isArray(first)) return first[0];
  if (typeof first === "string") return first;
  return "Не получилось отправить сообщение. Попробуйте ещё раз.";
}

export default function FeedbackPage() {
  const { user } = useAuth();
  const [entries, setEntries] = useState([]);
  const [feedLoading, setFeedLoading] = useState(true);
  const [feedError, setFeedError] = useState(false);
  const [reload, setReload] = useState(0);
  const [filter, setFilter] = useState("all");
  const [visibleCount, setVisibleCount] = useState(6);
  const [submitting, setSubmitting] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    kind: "review",
    name: "",
    contact: "",
    message: "",
    page_url: "",
    website: "",
  });

  useEffect(() => {
    if (!user) return;
    const name = [user.first_name, user.last_name].filter(Boolean).join(" ") || user.username;
    setForm((current) => ({ ...current, name: current.name || name || "" }));
  }, [user]);

  useEffect(() => {
    let active = true;
    setFeedLoading(true);
    setFeedError(false);
    apiRequest("/api/feedback/", { auth: false })
      .then(async (response) => {
        if (!response.ok) throw new Error();
        const data = await response.json();
        if (active) setEntries(data.entries || []);
      })
      .catch(() => { if (active) setFeedError(true); })
      .finally(() => { if (active) setFeedLoading(false); });
    return () => { active = false; };
  }, [reload]);

  const change = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
    setError("");
    setSent(false);
  };

  const submit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const response = await apiRequest("/api/feedback/", {
        method: "POST",
        body: JSON.stringify(form),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(getErrorMessage(data));
      if (data.entry) {
        setEntries((current) => [data.entry, ...current.filter((entry) => entry.id !== data.entry.id)]);
      }
      setFilter("all");
      setVisibleCount(6);
      setSent(true);
      setForm((current) => ({ ...current, message: "", page_url: "", website: "" }));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSubmitting(false);
    }
  };

  const filteredEntries = entries.filter((entry) => filter === "all" || entry.kind === filter);

  const currentKind = kinds.find((item) => item.value === form.kind);

  return (
    <main className="feedback-page">
      <section className="feedback-hero">
        <div className="container feedback-hero-inner">
          <span className="feedback-eyebrow">Помогите EidosAcademy стать лучше</span>
          <h1>Расскажите как есть</h1>
          <p>
            Нашли ошибку, придумали удобную функцию или просто хотите поделиться
            впечатлением? Мы читаем каждое сообщение.
          </p>
        </div>
      </section>

      <section className="container feedback-workspace">
        <form id="feedback-form" className="feedback-form" onSubmit={submit}>
          <div className="feedback-form-heading">
            <span>01</span>
            <div>
              <h2>Что у вас на уме?</h2>
              <p>Регистрация не обязательна. Можно написать анонимно.</p>
            </div>
          </div>

          <div className="feedback-kind-grid" role="radiogroup" aria-label="Тип сообщения">
            {kinds.map((kind) => (
              <label className={`feedback-kind ${form.kind === kind.value ? "active" : ""}`} key={kind.value}>
                <input type="radio" name="kind" value={kind.value} checked={form.kind === kind.value} onChange={change} />
                <span className="feedback-kind-icon" aria-hidden="true">{kind.icon}</span>
                <strong>{kind.title}</strong>
                <small>{kind.hint}</small>
              </label>
            ))}
          </div>

          <label className="feedback-field feedback-message-field">
            <span>{currentKind?.hint}</span>
            <textarea name="message" value={form.message} onChange={change} minLength="10" maxLength="2000" required placeholder="Пишите свободно — детали помогут быстрее разобраться." />
            <small>{form.message.length} / 2000</small>
          </label>

          <div className="feedback-fields-row">
            <label className="feedback-field">
              <span>Как к вам обращаться <em>необязательно</em></span>
              <input name="name" value={form.name} onChange={change} maxLength="80" placeholder="Имя или псевдоним" />
            </label>
            <label className="feedback-field">
              <span>Почта для ответа <em>необязательно</em></span>
              <input type="email" name="contact" value={form.contact} onChange={change} placeholder="you@example.com" />
              <small>Она останется приватной.</small>
            </label>
          </div>

          {form.kind === "bug" && (
            <label className="feedback-field">
              <span>Где возникла ошибка <em>необязательно</em></span>
              <input type="url" name="page_url" value={form.page_url} onChange={change} maxLength="500" placeholder="https://eidosacademy.ru/courses/..." />
            </label>
          )}

          <label className="feedback-honeypot" aria-hidden="true">
            Не заполняйте это поле
            <input name="website" value={form.website} onChange={change} tabIndex="-1" autoComplete="off" />
          </label>

          {error && <p className="feedback-alert error" role="alert">{error}</p>}
          {sent && <p className="feedback-alert success" role="status">Спасибо! Сообщение уже у нас — посмотрим его в ближайшее время.</p>}

          <div className="feedback-submit-row">
            <button className="feedback-submit" type="submit" disabled={submitting}>
              {submitting ? "Отправляем…" : "Отправить сообщение"}
            </button>
            <p>Сообщение появится на открытой доске без вашей почты.</p>
          </div>
        </form>

        <aside className="feedback-aside">
          <span className="feedback-aside-number">02</span>
          <h2>Что происходит дальше</h2>
          <ol>
            <li><span>1</span><p><strong>Читаем</strong>Сообщение попадает в панель команды.</p></li>
            <li><span>2</span><p><strong>Разбираемся</strong>Проверяем ошибку или оцениваем идею.</p></li>
            <li><span>3</span><p><strong>Отвечаем</strong>Если оставили почту и нужны детали.</p></li>
          </ol>
          <div className="feedback-aside-note">Каждый баг-репорт делает обучение чуть спокойнее для следующего человека.</div>
        </aside>
      </section>

      <section className="community-board" aria-labelledby="community-title">
        <div className="container community-container">
          <div className="community-intro">
            <div>
              <span className="community-eyebrow">Сделаем обучение лучше. Вместе.</span>
              <h2 id="community-title">Вы пишете — мы слышим.</h2>
              <p>Впечатления от обучения, хорошие идеи и то, что стоит исправить.</p>
            </div>
            <a className="community-write" href="#feedback-form">Оставить сообщение <span aria-hidden="true">↗</span></a>
          </div>
          <div className="community-panel">
            <div className="community-toolbar">
              <div className="community-filters" role="group" aria-label="Тип сообщений">
                {[{value: "all", title: "Все"}, {value: "review", title: "Отзывы"},
                  {value: "idea", title: "Идеи"}, {value: "bug", title: "Ошибки"}].map((item) => (
                  <button key={item.value} type="button" aria-pressed={filter === item.value}
                    onClick={() => { setFilter(item.value); setVisibleCount(6); }}>
                    {item.title}<span>{entries.filter((entry) => item.value === "all" || entry.kind === item.value).length}</span>
                  </button>
                ))}
              </div>
              <span className="community-order">Сначала новые</span>
            </div>
            {feedLoading ? <div className="community-empty" role="status">Загружаем сообщения…</div>
              : feedError ? <div className="community-empty" role="alert"><h3>Не удалось загрузить сообщения</h3>
                <button type="button" className="community-expand" onClick={() => setReload(reload + 1)}>Попробовать снова</button></div>
              : filteredEntries.length ? <>
                <div className="community-list">
                  {filteredEntries.slice(0, visibleCount).map((entry) => <FeedbackEntry entry={entry} key={entry.id} />)}
                </div>
                <div className="community-bottom">
                  <span>Показано {Math.min(visibleCount, filteredEntries.length)} из {filteredEntries.length}</span>
                  {visibleCount < filteredEntries.length && <button type="button" onClick={() => setVisibleCount(visibleCount + 6)}>Ещё сообщения ↓</button>}
                </div>
              </> : <div className="community-empty"><span aria-hidden="true">✦</span>
                <h3>{filter === "all" ? "Здесь начинается разговор" : "Пока без сообщений"}</h3>
                <p>{filter === "all" ? "Поделитесь первым впечатлением. Даже пара строк поможет нам." : "В этой категории ещё нет публикаций. Ваша может стать первой."}</p>
                <a href="#feedback-form">Написать сообщение ↗</a>
              </div>}
          </div>
        </div>
      </section>
    </main>
  );
}
