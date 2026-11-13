import { useEffect, useMemo, useRef, useState } from "react";

const MAX_RECENT = 6;

function readRecent(storageKey) {
  try {
    const value = JSON.parse(localStorage.getItem(storageKey) || "[]");
    return Array.isArray(value) ? value.filter((item) => typeof item === "string").slice(0, MAX_RECENT) : [];
  } catch {
    return [];
  }
}

export default function Search({
  className = "",
  type = "search",
  search = "",
  placeholder = "Поиск курса...",
  setSearch,
  suggestions = [],
  storageKey = "eidos-recent-course-searches",
}) {
  const rootRef = useRef(null);
  const [open, setOpen] = useState(false);
  const [recent, setRecent] = useState(() => readRecent(storageKey));
  const [activeIndex, setActiveIndex] = useState(-1);

  useEffect(() => {
    setRecent(readRecent(storageKey));
  }, [storageKey]);

  useEffect(() => {
    const close = (event) => {
      if (!rootRef.current?.contains(event.target)) setOpen(false);
    };
    document.addEventListener("pointerdown", close);
    return () => document.removeEventListener("pointerdown", close);
  }, []);

  useEffect(() => {
    const clean = search.trim();
    if (!clean) return undefined;
    const timer = window.setTimeout(() => {
      const current = readRecent(storageKey);
      const next = [clean, ...current.filter((item) => item.toLocaleLowerCase("ru-RU") !== clean.toLocaleLowerCase("ru-RU"))]
        .slice(0, MAX_RECENT);
      setRecent(next);
      localStorage.setItem(storageKey, JSON.stringify(next));
    }, 900);
    return () => window.clearTimeout(timer);
  }, [search, storageKey]);

  const normalized = search.trim().toLocaleLowerCase("ru-RU");
  const matches = useMemo(() => {
    if (!normalized) return [];
    const unique = [...new Set(suggestions.map((item) => String(item).trim()).filter(Boolean))];
    return unique
      .filter((item) => item.toLocaleLowerCase("ru-RU").startsWith(normalized))
      .slice(0, 6);
  }, [normalized, suggestions]);

  const saveRecent = (value) => {
    const clean = value.trim();
    if (!clean) return;
    const next = [clean, ...recent.filter((item) => item.toLocaleLowerCase("ru-RU") !== clean.toLocaleLowerCase("ru-RU"))]
      .slice(0, MAX_RECENT);
    setRecent(next);
    localStorage.setItem(storageKey, JSON.stringify(next));
  };

  const choose = (value) => {
    setSearch(value);
    saveRecent(value);
    setOpen(false);
  };

  const removeRecent = (value) => {
    const next = recent.filter((item) => item !== value);
    setRecent(next);
    localStorage.setItem(storageKey, JSON.stringify(next));
  };

  const showRecent = open && !normalized && recent.length > 0;
  const showMatches = open && normalized && matches.length > 0;
  const visibleOptions = showRecent ? recent : showMatches ? matches : [];
  const listId = `${storageKey.replace(/[^a-z0-9_-]/gi, "-")}-options`;

  useEffect(() => {
    setActiveIndex(-1);
  }, [search, open]);

  return (
    <div className={`relative ${className}`} ref={rootRef}>
      <div className="relative flex items-center">
        <span className="pointer-events-none absolute left-4 text-xl text-[var(--muted)]" aria-hidden="true">⌕</span>
        <input
          className="w-full rounded-2xl border border-[var(--line)] bg-[var(--white)] py-4 pr-12 pl-12 text-[var(--ink)] shadow-[0_10px_30px_rgba(34,46,80,.07)] outline-none transition placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:ring-4 focus:ring-blue-500/10"
          type={type}
          value={search}
          aria-label="Поиск курса"
          aria-expanded={showRecent || showMatches}
          aria-controls={listId}
          aria-activedescendant={activeIndex >= 0 ? `${listId}-${activeIndex}` : undefined}
          aria-autocomplete="list"
          autoComplete="off"
          placeholder={placeholder}
          onFocus={() => setOpen(true)}
          onChange={(event) => { setSearch(event.target.value); setOpen(true); }}
          onKeyDown={(event) => {
            if (event.key === "ArrowDown" && visibleOptions.length) {
              event.preventDefault();
              setOpen(true);
              setActiveIndex((index) => (index + 1) % visibleOptions.length);
              return;
            }
            if (event.key === "ArrowUp" && visibleOptions.length) {
              event.preventDefault();
              setOpen(true);
              setActiveIndex((index) => index <= 0 ? visibleOptions.length - 1 : index - 1);
              return;
            }
            if (event.key === "Enter") {
              event.preventDefault();
              if (activeIndex >= 0 && visibleOptions[activeIndex]) choose(visibleOptions[activeIndex]);
              else saveRecent(search);
              setOpen(false);
            }
            if (event.key === "Escape") { setOpen(false); setActiveIndex(-1); }
          }}
        />
        {search && (
          <button type="button" className="absolute right-3 grid h-9 w-9 place-items-center rounded-lg text-xl text-[var(--muted)] transition hover:bg-[var(--paper)] hover:text-[var(--ink)]" aria-label="Очистить поиск" onClick={() => { setSearch(""); setOpen(true); }}>
            ×
          </button>
        )}
      </div>

      {(showRecent || showMatches) && (
        <div className="absolute inset-x-0 top-[calc(100%_+_8px)] z-40 overflow-hidden rounded-2xl border border-[var(--line)] bg-[var(--white)] p-2 shadow-[0_24px_60px_rgba(15,23,42,.18)]" id={listId} role="listbox">
          <div className="px-3 py-2 text-xs font-extrabold uppercase tracking-wider text-[var(--muted)]">{showRecent ? "Недавние запросы" : "Предложения"}</div>
          {showRecent && recent.map((item, index) => (
            <div className="flex items-center gap-1" key={item}>
              <button type="button" id={`${listId}-${index}`} className={`flex min-w-0 flex-1 items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-[var(--ink)] transition ${activeIndex === index ? "bg-[var(--blue-soft)] text-[var(--blue)]" : "hover:bg-[var(--paper)]"}`} role="option" aria-selected={activeIndex === index} onMouseEnter={() => setActiveIndex(index)} onClick={() => choose(item)}>
                <span aria-hidden="true">↶</span>{item}
              </button>
              <button type="button" className="grid h-9 w-9 flex-none place-items-center rounded-lg text-[var(--muted)] hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-950/30" aria-label={`Удалить запрос «${item}»`} onClick={() => removeRecent(item)}>×</button>
            </div>
          ))}
          {showMatches && matches.map((item, index) => (
            <button type="button" id={`${listId}-${index}`} className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-[var(--ink)] transition ${activeIndex === index ? "bg-[var(--blue-soft)] text-[var(--blue)]" : "hover:bg-[var(--paper)]"}`} role="option" aria-selected={activeIndex === index} key={item} onMouseEnter={() => setActiveIndex(index)} onClick={() => choose(item)}>
              <span aria-hidden="true">⌕</span>{item}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
