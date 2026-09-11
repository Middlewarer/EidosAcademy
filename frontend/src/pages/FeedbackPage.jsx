import { useEffect, useState } from "react";
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
  const isLong = entry.message.length > 260;
  const formattedDate = new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date(entry.created_at));

  return (
    <article className={`feedback-entry ${expanded ? "is-expanded" : ""}`}>
      <div className="feedback-entry-meta">
        <span className={`feedback-kind-badge ${entry.kind}`}>{entry.kind_label}</span>
        <span className={`feedback-status ${statusClass[entry.status] || "neutral"}`}>{entry.status_label}</span>
      </div>
      <div className="feedback-entry-body">
        <span className="feedback-quote" aria-hidden="true">“</span>
        <p className={expanded ? "is-expanded" : ""}>{entry.message}</p>
        {isLong && (
          <button type="button" className="feedback-entry-toggle" onClick={() => setExpanded((value) => !value)}>
            {expanded ? "Свернуть" : "Читать полностью"}
          </button>
        )}
      </div>
      <footer>
        <span className="feedback-author-avatar" aria-hidden="true">{entry.author.charAt(0).toUpperCase()}</span>
        <span className="feedback-author">
          <strong>{entry.author}</strong>
          <time dateTime={entry.created_at}>{formattedDate}</time>
        </span>
      </footer>
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
    apiRequest("/api/feedback/", { auth: false })
      .then(async (response) => {
        if (!response.ok) throw new Error();
        const data = await response.json();
        if (active) setEntries(data.entries || []);
      })
      .catch(() => {})
      .finally(() => { if (active) setFeedLoading(false); });
    return () => { active = false; };
  }, []);

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
      setSent(true);
      setForm((current) => ({ ...current, message: "", page_url: "", website: "" }));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSubmitting(false);
    }
  };

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
        <form className="feedback-form" onSubmit={submit}>
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

      <section className="feedback-community">
        <div className="container">
          <div className="feedback-section-heading">
            <div><span className="feedback-eyebrow">Открытая доска</span><h2>Голос сообщества</h2></div>
            <p>Опубликованные отзывы, идеи и ошибки, над которыми идёт работа.</p>
          </div>
          {feedLoading ? (
            <p className="feedback-empty">Загружаем сообщения…</p>
          ) : entries.length ? (
            <div className="feedback-entry-grid">
              {entries.map((entry) => (
                <FeedbackEntry entry={entry} key={entry.id} />
              ))}
            </div>
          ) : (
            <p className="feedback-empty">Здесь скоро появятся первые сообщения. Можете стать первым.</p>
          )}
        </div>
      </section>
    </main>
  );
}
