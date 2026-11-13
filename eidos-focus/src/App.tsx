import { useEffect, useState } from "react";
import { ArrowRight, BookOpen, BriefcaseBusiness, Check, ChevronRight, CirclePause, Flame, LayoutDashboard, Play, Plus, RotateCcw, Send, Sparkles, Target, Timer, Trophy } from "lucide-react";
import { api } from "./api";
import type { Dashboard, MissionItem, TimerState } from "./types";

const kindLabels: Record<string, string> = { learn: "Учёба", prove: "Проект", apply: "Карьера" };
const fmt = (seconds: number) => `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;

function App() {
  const widgetMode = new URLSearchParams(window.location.search).has("widget");
  if (widgetMode) return <PomodoroWidget/>;
  return <MainApp/>;
}

function MainApp() {
  const [data, setData] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");
  const [tab, setTab] = useState("today");
  const [timer, setTimer] = useState<TimerState | null>(null);
  const [missionDraft, setMissionDraft] = useState("");
  const [commitOpen, setCommitOpen] = useState(false);

  const refresh = () => api.dashboard().then(setData).catch(e => setError(String(e.message || e)));
  useEffect(() => { void refresh(); }, []);
  useEffect(() => {
    let alive = true;
    const update = () => api.timer().then(value => alive && setTimer(value)).catch(() => {});
    void update();
    const poll = window.setInterval(update, 500);
    return () => { alive = false; window.clearInterval(poll); };
  }, []);

  const activeTask = data?.mission.items.find(x => !x.done)?.title || data?.commitment.outcome || "Главная задача дня";
  const remaining = timer?.remaining ?? 50 * 60;
  const running = timer?.running ?? false;
  const timerAction = async (action: "start" | "pause" | "reset") => {
    const state = await api.timerAction(action, activeTask);
    setTimer(state);
    if (action === "start") await window.pywebview?.api?.open_widget?.();
    if (action !== "start") void refresh();
  };

  if (error) return <div className="fatal"><Sparkles/><h1>Eidos не смог открыть данные</h1><p>{error}</p><button onClick={refresh}>Повторить</button></div>;
  if (!data) return <div className="loading"><span/><p>Собираем день в фокус…</p></div>;

  const addMission = async () => {
    const title = missionDraft.trim();
    if (!title || data.mission.items.length >= 3) return;
    const item: MissionItem = { id: crypto.randomUUID(), title, kind: data.mission.items.length === 2 ? "apply" : "learn", done: false };
    setMissionDraft(""); setData(await api.mission([...data.mission.items, item]));
  };
  const toggleMission = async (id: string) => setData(await api.mission(data.mission.items.map(x => x.id === id ? { ...x, done: !x.done } : x)));
  const score = Math.round((data.metrics.resume_percent + data.metrics.interview_score + Math.min(100, data.metrics.applications_week * 12)) / 3);

  return <div className="app-shell">
    <aside>
      <div className="brand"><div className="mark">E</div><div><b>Eidos</b><span>career focus</span></div></div>
      <nav>
        <Nav active={tab === "today"} icon={<LayoutDashboard/>} label="Сегодня" onClick={() => setTab("today")}/>
        <Nav active={tab === "tracks"} icon={<BookOpen/>} label="Треки" onClick={() => setTab("tracks")}/>
        <Nav active={tab === "career"} icon={<BriefcaseBusiness/>} label="Карьера" onClick={() => setTab("career")}/>
        <Nav active={tab === "progress"} icon={<Trophy/>} label="Прогресс" onClick={() => setTab("progress")}/>
      </nav>
      <div className="side-spacer"/>
      <div className="streak"><Flame/><div><b>{data.metrics.streak} дней</b><span>текущая серия</span></div></div>
      <div className="data-note"><span className="status-dot"/>Данные синхронизированы<small title={data.state_path}>{data.compatibility.curriculum_loaded ? "Все модули подключены" : "Режим совместимости"}</small></div>
    </aside>

    <main>
      {tab === "today" && <>
        <header><div><div className="eyebrow">{new Date(data.date + "T12:00:00").toLocaleDateString("ru-RU", { weekday: "long", day: "numeric", month: "long" })}</div><h1>Что приблизит тебя к офферу сегодня?</h1><p>Один ясный результат. Три действия. Никакого шума.</p></div><button className="ghost" onClick={() => setCommitOpen(true)}><Target/> Контракт дня</button></header>

        {!data.commitment.signed && <section className="contract-banner"><div className="contract-icon"><Target/></div><div><span>Начни осознанно</span><h3>Зафиксируй результат, который обязан случиться сегодня</h3></div><button onClick={() => setCommitOpen(true)}>Заключить контракт <ArrowRight/></button></section>}

        <div className="grid-top">
          <section className="panel mission"><PanelTitle icon={<Sparkles/>} title="Миссия дня" meta={`${data.mission.items.filter(x=>x.done).length} / 3`}/>
            <div className="mission-list">
              {data.mission.items.map((item, i) => <button className={`mission-row ${item.done ? "done" : ""}`} key={item.id} onClick={() => toggleMission(item.id)}><span className="check">{item.done && <Check/>}</span><span className="mission-num">0{i+1}</span><span className="mission-copy"><b>{item.title}</b><small>{kindLabels[item.kind] || "Фокус"}</small></span><ChevronRight/></button>)}
              {data.mission.items.length < 3 && <div className="mission-add"><Plus/><input value={missionDraft} onChange={e=>setMissionDraft(e.target.value)} onKeyDown={e=>e.key === "Enter" && void addMission()} placeholder="Добавить конкретное действие…"/><button onClick={addMission}>Добавить</button></div>}
            </div>
          </section>

          <section className="panel focus-card"><PanelTitle icon={<Timer/>} title="Фокус" meta={running ? "сейчас" : "готов"}/>
            <div className={`timer-ring ${running ? "active" : ""}`} style={{"--progress": `${(1 - remaining/(timer?.duration || 3000))*360}deg`} as React.CSSProperties}><div><strong>{fmt(remaining)}</strong><span>{timer?.task || activeTask}</span></div></div>
            <div className="timer-actions"><button className="round secondary" onClick={() => void timerAction("reset")} aria-label="Сбросить"><RotateCcw/></button><button className="focus-button" onClick={() => void timerAction(running ? "pause" : "start")}>{running ? <CirclePause/> : <Play/>}{running ? "Пауза" : "Начать фокус"}</button></div>
          </section>
        </div>

        <div className="metrics-row">
          <Metric value={`${Math.floor(data.metrics.focus_minutes/60)}ч ${data.metrics.focus_minutes%60}м`} label="Фокус сегодня" hint={`из ${Math.round(data.metrics.target_minutes/60)} часов`} accent="mint"/>
          <Metric value={String(data.metrics.completed_tasks)} label="Закрыто задач" hint="за всё время" accent="violet"/>
          <Metric value={String(data.metrics.applications_week)} label="Откликов" hint="за эту неделю" accent="blue"/>
          <Metric value={`${score}%`} label="Готовность" hint="к следующему этапу" accent="amber"/>
        </div>

        <section className="panel trajectory"><PanelTitle icon={<BriefcaseBusiness/>} title="Траектория к офферу" meta="Learn → Prove → Apply"/><div className="trajectory-grid">
          <Stage n="01" title="Учись" text="Следующая тема из технического трека" value={data.tracks.reduce((s,t)=>s+t.done,0)} suffix=" задач"/>
          <Stage n="02" title="Докажи" text="Проекты и воспроизводимые результаты" value={data.metrics.project_steps} suffix=" шагов"/>
          <Stage n="03" title="Откликайся" text="Качественные целевые отклики" value={data.metrics.applications_week} suffix=" за неделю" hot/>
          <Stage n="04" title="Интервью" text="Практика ответов без подсказок" value={data.metrics.interview_score} suffix=" / 100"/>
        </div></section>
      </>}

      {tab === "tracks" && <Page title="Учебные треки" subtitle="Существующий прогресс, собранный в одном спокойном представлении."><div className="track-grid">{data.tracks.map(track => <div className="track-card" key={track.id} style={{"--track": track.color} as React.CSSProperties}><span>{track.id.toUpperCase()}</span><h3>{track.title}</h3><div className="progress"><i style={{width: `${track.total ? track.done/track.total*100 : 0}%`}}/></div><p>{track.done} из {track.total || "—"} заданий</p></div>)}</div></Page>}
      {tab === "career" && <Career data={data} onUpdate={setData}/>} 
      {tab === "progress" && <Page title="Ритм работы" subtitle="Не идеальная серия, а устойчивое возвращение к важному."><div className="panel heat-panel"><PanelTitle icon={<Flame/>} title={`${data.metrics.streak} дней в серии`} meta="последние 35 дней"/><div className="heatmap">{data.heatmap.map(day => <span key={day.date} title={`${day.date}: ${day.minutes} мин`} data-level={Math.min(4, Math.ceil(day.minutes/30))}/>)}</div></div><div className="metrics-row progress-metrics"><Metric value={`${data.metrics.interview_score}`} label="Интервью" hint="средний балл" accent="violet"/><Metric value={`${data.metrics.resume_percent}%`} label="Резюме" hint="готовность" accent="blue"/><Metric value={`${data.applications.length}`} label="Отклики" hint="всего" accent="mint"/></div></Page>}
    </main>
    {commitOpen && <CommitmentModal value={data.commitment} onClose={()=>setCommitOpen(false)} onSave={async value => { setData(await api.commitment(value)); setCommitOpen(false); }}/>} 
  </div>;
}

function Nav({active, icon, label, onClick}:{active:boolean;icon:React.ReactNode;label:string;onClick:()=>void}) { return <button className={active ? "active" : ""} onClick={onClick}>{icon}<span>{label}</span></button> }
function PanelTitle({icon,title,meta}:{icon:React.ReactNode;title:string;meta:string}) { return <div className="panel-title"><div>{icon}<h2>{title}</h2></div><span>{meta}</span></div> }
function Metric({value,label,hint,accent}:{value:string;label:string;hint:string;accent:string}) { return <div className={`metric ${accent}`}><strong>{value}</strong><b>{label}</b><span>{hint}</span></div> }
function Stage({n,title,text,value,suffix,hot=false}:{n:string;title:string;text:string;value:number;suffix:string;hot?:boolean}) { return <div className={`stage ${hot?"hot":""}`}><span>{n}</span><div><h3>{title}</h3><p>{text}</p></div><b>{value}{suffix}</b></div> }
function Page({title,subtitle,children}:{title:string;subtitle:string;children:React.ReactNode}) { return <><header><div><div className="eyebrow">Eidos workspace</div><h1>{title}</h1><p>{subtitle}</p></div></header>{children}</> }
function Career({data,onUpdate}:{data:Dashboard;onUpdate:(d:Dashboard)=>void}) { const [company,setCompany]=useState(""); const [role,setRole]=useState(""); return <Page title="Карьерные действия" subtitle="Вакансии превращаются в следующие понятные шаги."><section className="panel career-panel"><PanelTitle icon={<Send/>} title="Быстрый отклик" meta={`${data.metrics.applications_week} на этой неделе`}/><div className="quick-form"><input value={company} onChange={e=>setCompany(e.target.value)} placeholder="Компания"/><input value={role} onChange={e=>setRole(e.target.value)} placeholder="Позиция"/><button onClick={async()=>{if(company&&role){onUpdate(await api.application(company,role));setCompany("");setRole("")}}}>Добавить</button></div><div className="application-list">{data.applications.slice(0,8).map(x=><div key={x.id}><span>{x.company.slice(0,1).toUpperCase()}</span><div><b>{x.company}</b><small>{x.role}</small></div><em>{x.status || "saved"}</em></div>)}</div></section></Page> }
function CommitmentModal({value,onClose,onSave}:{value:Dashboard["commitment"];onClose:()=>void;onSave:(v:Dashboard["commitment"])=>void}) { const [draft,setDraft]=useState(value); return <div className="modal-backdrop" onMouseDown={e=>e.target===e.currentTarget&&onClose()}><div className="modal"><div className="eyebrow">TODAY'S CONTRACT</div><h2>Обещание самому себе</h2><label>До конца дня я закончу<input autoFocus value={draft.outcome} onChange={e=>setDraft({...draft,outcome:e.target.value})} placeholder="Один измеримый результат"/></label><div className="form-row"><label>Дедлайн<input type="time" value={draft.deadline} onChange={e=>setDraft({...draft,deadline:e.target.value})}/></label><label>Фокус, минут<input type="number" min="25" step="25" value={draft.focus_minutes} onChange={e=>setDraft({...draft,focus_minutes:Number(e.target.value)})}/></label></div><label>Что может отвлечь?<input value={draft.distraction} onChange={e=>setDraft({...draft,distraction:e.target.value})} placeholder="Telegram, YouTube, перфекционизм…"/></label><div className="modal-actions"><button className="ghost" onClick={onClose}>Отмена</button><button onClick={()=>draft.outcome.trim()&&onSave({...draft,signed:true})}>Зафиксировать <Check/></button></div></div></div> }

function PomodoroWidget() {
  const [timer, setTimer] = useState<TimerState>({ duration: 3000, remaining: 3000, running: false, task: "Фокус", mode: "focus" });
  useEffect(() => {
    document.body.classList.add("widget-mode");
    let alive = true;
    const update = () => api.timer().then(value => alive && setTimer(value)).catch(() => {});
    void update();
    const poll = window.setInterval(update, 400);
    return () => { alive = false; window.clearInterval(poll); document.body.classList.remove("widget-mode"); };
  }, []);
  const act = async (action: "start" | "pause" | "reset" | "complete") => setTimer(await api.timerAction(action, timer.task));
  const progress = Math.max(0, Math.min(1, 1 - timer.remaining / Math.max(1, timer.duration)));
  return <div className="pomodoro-widget">
    <div className="widget-glow"/>
    <div className="widget-head"><span><i/> EIDOS FOCUS</span><button onClick={() => window.pywebview?.api?.hide_widget?.()}>×</button></div>
    <div className="widget-body">
      <div className="widget-ring" style={{"--widget-progress": `${progress * 360}deg`} as React.CSSProperties}><div><strong>{fmt(timer.remaining)}</strong><small>{timer.running ? "в фокусе" : "пауза"}</small></div></div>
      <div className="widget-copy"><span>Сейчас главное</span><h2>{timer.task || "Выбери задачу в Eidos"}</h2><div className="widget-controls"><button className="widget-play" onClick={() => void act(timer.running ? "pause" : "start")}>{timer.running ? <CirclePause/> : <Play/>}{timer.running ? "Пауза" : "Продолжить"}</button><button title="Завершить сессию" onClick={() => void act("complete")}><Check/></button><button title="Открыть Eidos" onClick={() => window.pywebview?.api?.show_main?.()}><ArrowRight/></button></div></div>
    </div>
  </div>;
}

export default App;
