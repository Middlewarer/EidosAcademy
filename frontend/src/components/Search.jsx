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
  className = "courses-search",
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
    <div className={`${className} search-with-history`} ref={rootRef}>
      <div className="search-input-wrap">
        <span className="search-icon" aria-hidden="true">⌕</span>
        <input
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
          <button type="button" className="search-clear" aria-label="Очистить поиск" onClick={() => { setSearch(""); setOpen(true); }}>
            ×
          </button>
        )}
      </div>

      {(showRecent || showMatches) && (
        <div className="search-popover" id={listId} role="listbox">
          <div className="search-popover-title">{showRecent ? "Недавние запросы" : "Предложения"}</div>
          {showRecent && recent.map((item, index) => (
            <div className="search-recent-row" key={item}>
              <button type="button" id={`${listId}-${index}`} className="search-option" role="option" aria-selected={activeIndex === index} onMouseEnter={() => setActiveIndex(index)} onClick={() => choose(item)}>
                <span aria-hidden="true">↶</span>{item}
              </button>
              <button type="button" className="search-remove" aria-label={`Удалить запрос «${item}»`} onClick={() => removeRecent(item)}>×</button>
            </div>
          ))}
          {showMatches && matches.map((item, index) => (
            <button type="button" id={`${listId}-${index}`} className="search-option" role="option" aria-selected={activeIndex === index} key={item} onMouseEnter={() => setActiveIndex(index)} onClick={() => choose(item)}>
              <span aria-hidden="true">⌕</span>{item}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
