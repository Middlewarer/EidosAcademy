import { useEffect, useState } from "react";
import { AlertTriangle, ArrowRight, BookOpen, BriefcaseBusiness, Check, ChevronRight, CirclePause, Clock3, CloudRain, Copy, ExternalLink, Flame, Layers3, LayoutDashboard, Play, Plus, RotateCcw, Send, Settings2, Sparkles, Timer, Trophy, Volume2, VolumeX, Waves, X } from "lucide-react";
import { api } from "./api";
import type { Dashboard, LearningIndex, MissionItem, PomodoroSettings, TimerState, TopicDetail } from "./types";

const kindLabels: Record<string, string> = { learn: "Учёба", prove: "Проект", apply: "Карьера" };
const fmt = (seconds: number) => `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;

function App() {
  const params = new URLSearchParams(window.location.search);
  const widgetMode = params.has("widget");
  if (params.has("prompts")) return <PromptLab/>;
  if (widgetMode) return <PomodoroWidget/>;
  return <MainApp/>;
}

function MainApp() {
  const [data, setData] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");
  const [tab, setTab] = useState("today");
  const [timer, setTimer] = useState<TimerState | null>(null);
  const [missionDraft, setMissionDraft] = useState("");
  const [pomodoroOpen, setPomodoroOpen] = useState(false);

  const refresh = () => api.dashboard().then(setData).catch(e => setError(String(e.message || e)));
  useEffect(() => { void refresh(); }, []);
  useEffect(() => {
    let alive = true;
    const update = () => api.timer().then(value => alive && setTimer(value)).catch(() => {});
    void update();
    const poll = window.setInterval(update, 500);
    return () => { alive = false; window.clearInterval(poll); };
  }, []);

  const activeTask = data?.mission.items.find(x => !x.done)?.title || "Главная задача дня";
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
    <AmbientSound active={running && timer?.mode === "focus"} settings={data.pomodoro}/>
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
        <header><div><div className="eyebrow">{new Date(data.date + "T12:00:00").toLocaleDateString("ru-RU", { weekday: "long", day: "numeric", month: "long" })}</div><h1>Что приблизит тебя к офферу сегодня?</h1><p>Один ясный результат. Три действия. Никакого шума.</p></div></header>

        <PaceBanner pace={data.pace}/>

        <div className="grid-top">
          <section className="panel mission"><PanelTitle icon={<Sparkles/>} title="Миссия дня" meta={`${data.mission.items.filter(x=>x.done).length} / 3`}/>
            <div className="mission-list">
              {data.mission.items.map((item, i) => <button className={`mission-row ${item.done ? "done" : ""}`} key={item.id} onClick={() => toggleMission(item.id)}><span className="check">{item.done && <Check/>}</span><span className="mission-num">0{i+1}</span><span className="mission-copy"><b>{item.title}</b><small>{kindLabels[item.kind] || "Фокус"}</small></span><ChevronRight/></button>)}
              {data.mission.items.length < 3 && <div className="mission-add"><Plus/><input value={missionDraft} onChange={e=>setMissionDraft(e.target.value)} onKeyDown={e=>e.key === "Enter" && void addMission()} placeholder="Добавить конкретное действие…"/><button onClick={addMission}>Добавить</button></div>}
            </div>
          </section>

          <section className={`panel focus-card ${timer?.mode === "break" ? "break-mode" : ""}`}><div className="panel-title focus-title"><div><Timer/><h2>{timer?.mode === "break" ? "Перерыв" : "Фокус"}</h2></div><button onClick={()=>setPomodoroOpen(true)}><Settings2/>{data.pomodoro.focus_minutes}/{data.pomodoro.break_minutes}</button></div>
            <div className={`timer-ring ${running ? "active" : ""}`} style={{"--progress": `${(1 - remaining/(timer?.duration || 3600))*360}deg`} as React.CSSProperties}><div><strong>{fmt(remaining)}</strong><span>{timer?.mode === "break" ? "Время восстановиться" : (timer?.task || activeTask)}</span></div></div>
            <div className="timer-actions"><button className="round secondary" onClick={() => void timerAction("reset")} aria-label="Сбросить"><RotateCcw/></button><button className="focus-button" onClick={() => void timerAction(running ? "pause" : "start")}>{running ? <CirclePause/> : <Play/>}{running ? "Пауза" : timer?.mode === "break" ? "Начать перерыв" : "Начать фокус"}</button></div>
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

      {tab === "tracks" && <TracksWorkspace/>}
      {tab === "career" && <Career data={data} onUpdate={setData}/>} 
      {tab === "progress" && <Page title="Ритм работы" subtitle="Не идеальная серия, а устойчивое возвращение к важному."><div className="panel heat-panel"><PanelTitle icon={<Flame/>} title={`${data.metrics.streak} дней в серии`} meta="последние 35 дней"/><div className="heatmap">{data.heatmap.map(day => <span key={day.date} title={`${day.date}: ${day.minutes} мин`} data-level={Math.min(4, Math.ceil(day.minutes/30))}/>)}</div></div><div className="metrics-row progress-metrics"><Metric value={`${data.metrics.interview_score}`} label="Интервью" hint="средний балл" accent="violet"/><Metric value={`${data.metrics.resume_percent}%`} label="Резюме" hint="готовность" accent="blue"/><Metric value={`${data.applications.length}`} label="Отклики" hint="всего" accent="mint"/></div></Page>}
    </main>
    {pomodoroOpen&&<PomodoroSettingsModal value={data.pomodoro} onClose={()=>setPomodoroOpen(false)} onSave={async value=>{setData(await api.savePomodoroSettings(value));setTimer(await api.timer());setPomodoroOpen(false)}}/>}
  </div>;
}

function Nav({active, icon, label, onClick}:{active:boolean;icon:React.ReactNode;label:string;onClick:()=>void}) { return <button className={active ? "active" : ""} onClick={onClick}>{icon}<span>{label}</span></button> }
function PanelTitle({icon,title,meta}:{icon:React.ReactNode;title:string;meta:string}) { return <div className="panel-title"><div>{icon}<h2>{title}</h2></div><span>{meta}</span></div> }
function Metric({value,label,hint,accent}:{value:string;label:string;hint:string;accent:string}) { return <div className={`metric ${accent}`}><strong>{value}</strong><b>{label}</b><span>{hint}</span></div> }
function Stage({n,title,text,value,suffix,hot=false}:{n:string;title:string;text:string;value:number;suffix:string;hot?:boolean}) { return <div className={`stage ${hot?"hot":""}`}><span>{n}</span><div><h3>{title}</h3><p>{text}</p></div><b>{value}{suffix}</b></div> }
function Page({title,subtitle,children}:{title:string;subtitle:string;children:React.ReactNode}) { return <><header><div><div className="eyebrow">Eidos workspace</div><h1>{title}</h1><p>{subtitle}</p></div></header>{children}</> }
function Career({data,onUpdate}:{data:Dashboard;onUpdate:(d:Dashboard)=>void}) { const [company,setCompany]=useState(""); const [role,setRole]=useState(""); return <Page title="Карьерные действия" subtitle="Вакансии превращаются в следующие понятные шаги."><section className="panel career-panel"><PanelTitle icon={<Send/>} title="Быстрый отклик" meta={`${data.metrics.applications_week} на этой неделе`}/><div className="quick-form"><input value={company} onChange={e=>setCompany(e.target.value)} placeholder="Компания"/><input value={role} onChange={e=>setRole(e.target.value)} placeholder="Позиция"/><button onClick={async()=>{if(company&&role){onUpdate(await api.application(company,role));setCompany("");setRole("")}}}>Добавить</button></div><div className="application-list">{data.applications.slice(0,8).map(x=><div key={x.id}><span>{x.company.slice(0,1).toUpperCase()}</span><div><b>{x.company}</b><small>{x.role}</small></div><em>{x.status || "saved"}</em></div>)}</div></section></Page> }
function PaceBanner({pace}:{pace:Dashboard["pace"]}) {
  const behind = pace.status === "behind";
  const target = new Date(pace.target_date + "T12:00:00").toLocaleDateString("ru-RU", { day:"numeric", month:"long" });
  return <section className={`pace-banner ${pace.status}`}><div className="pace-signal">{behind?<AlertTriangle/>:<Flame/>}</div><div className="pace-copy"><span>{behind?"ТЕМП НИЖЕ ПЛАНА":pace.status==="ahead"?"ИДЁШЬ С ОПЕРЕЖЕНИЕМ":"ТЕМП В НОРМЕ"}</span><h3>{behind?`Ты отстаёшь на ${pace.gap_tasks} заданий. Нужно поднажать.`:pace.status==="ahead"?"Ты впереди графика — сохрани этот ритм.":"Ты идёшь по графику. Не сбавляй темп."}</h3><p>Сейчас {pace.actual_tasks} из {pace.total_tasks}, по плану — {pace.expected_tasks}. Чтобы закончить к {target}: <b>{pace.tasks_per_day_needed} заданий в день</b>.</p></div><div className="pace-chart"><div><i style={{width:`${pace.actual_percent}%`}}/><em style={{left:`${pace.expected_percent}%`}}/></div><span><b>{pace.actual_percent}%</b> выполнено</span><small>{pace.days_remaining} дней осталось</small></div></section>;
}

function AmbientSound({active,settings}:{active:boolean;settings:PomodoroSettings}) {
  useEffect(()=>{
    if(!active||settings.ambient_sound==="none"||settings.ambient_volume<=0)return;
    const files={rain:"/audio/rain-long.mp3",fire:"/audio/campfire-night.mp3",ocean:"/audio/ocean-waves.mp3"} as const;
    const audio=new Audio(files[settings.ambient_sound]);
    audio.loop=true;audio.preload="auto";audio.volume=Math.min(1,Math.max(0,settings.ambient_volume/100));
    void audio.play().catch(()=>{});
    return()=>{audio.pause();audio.src=""};
  },[active,settings.ambient_sound,settings.ambient_volume]);
  return null;
}

function PomodoroSettingsModal({value,onClose,onSave}:{value:PomodoroSettings;onClose:()=>void;onSave:(value:PomodoroSettings)=>void}) {
  const [draft,setDraft]=useState(value);
  const [previewing,setPreviewing]=useState(false);
  const presets=[[25,5],[50,10],[60,10],[90,15]];
  const sounds:[PomodoroSettings["ambient_sound"],string,React.ReactNode][]=[["none","Тишина",<VolumeX/>],["rain","Дождь",<CloudRain/>],["fire","Костёр",<Flame/>],["ocean","Океан",<Waves/>]];
  return <div className="modal-backdrop" onMouseDown={e=>e.target===e.currentTarget&&onClose()}><div className="modal pomodoro-settings"><div className="settings-head"><div><div className="eyebrow">FOCUS RHYTHM</div><h2>Настройка Pomodoro</h2></div><button onClick={onClose}><X/></button></div><p className="settings-lead">Собери спокойный рабочий ритм под себя. Настройки сохранятся для следующих запусков.</p>
    <section><label className="settings-label">Быстрый ритм</label><div className="preset-grid">{presets.map(([focus,rest])=><button key={focus} className={draft.focus_minutes===focus&&draft.break_minutes===rest?"active":""} onClick={()=>setDraft({...draft,focus_minutes:focus,break_minutes:rest})}><b>{focus}</b><span>фокус</span><i>+</i><b>{rest}</b><span>отдых</span></button>)}</div></section>
    <section className="duration-grid"><label>Работа, минут<input type="number" min="10" max="180" value={draft.focus_minutes} onChange={e=>setDraft({...draft,focus_minutes:Number(e.target.value)})}/></label><label>Перерыв, минут<input type="number" min="1" max="60" value={draft.break_minutes} onChange={e=>setDraft({...draft,break_minutes:Number(e.target.value)})}/></label></section>
    <AmbientSound active={previewing} settings={draft}/>
    <section><div className="sound-heading"><label className="settings-label">Фоновая атмосфера</label><button disabled={draft.ambient_sound==="none"} onClick={()=>setPreviewing(current=>!current)}>{previewing?<VolumeX/>:<Volume2/>}{previewing?"Остановить":"Прослушать"}</button></div><div className="sound-grid">{sounds.map(([id,label,icon])=><button key={id} className={draft.ambient_sound===id?"active":""} onClick={()=>{setPreviewing(false);setDraft({...draft,ambient_sound:id})}}>{icon}<span>{label}</span></button>)}</div></section>
    <section className="volume-row"><Volume2/><label><span>Громкость <b>{draft.ambient_volume}%</b></span><input type="range" min="0" max="100" value={draft.ambient_volume} onChange={e=>setDraft({...draft,ambient_volume:Number(e.target.value)})}/></label></section>
    <label className="switch-row"><input type="checkbox" checked={draft.auto_start_break} onChange={e=>setDraft({...draft,auto_start_break:e.target.checked})}/><span><b>Автоматически начинать перерыв</b><small>После завершения фокус-сессии таймер сразу переключится на отдых.</small></span></label>
    <div className="modal-actions"><button className="ghost" onClick={onClose}>Отмена</button><button onClick={()=>onSave(draft)}>Сохранить ритм <Check/></button></div>
  </div></div>;
}

function TracksWorkspace() {
  const [index, setIndex] = useState<LearningIndex | null>(null);
  const [selectedTrack, setSelectedTrack] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("");
  const [detail, setDetail] = useState<TopicDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState("");
  useEffect(() => { api.learning().then(value => { setIndex(value); const track = value.tracks[0]; setSelectedTrack(track?.id || ""); setSelectedTopic(track?.topics[0]?.id || ""); }).finally(() => setLoading(false)); }, []);
  useEffect(() => { if (!selectedTrack || !selectedTopic) return; setDetail(null); api.topic(selectedTrack, selectedTopic).then(setDetail); }, [selectedTrack, selectedTopic]);
  const track = index?.tracks.find(item => item.id === selectedTrack);
  const chooseTrack = (id: string) => { const next = index?.tracks.find(item => item.id === id); setSelectedTrack(id); setSelectedTopic(next?.topics[0]?.id || ""); };
  const copy = async (text: string, key: string) => { await navigator.clipboard.writeText(text); setCopied(key); window.setTimeout(() => setCopied(""), 1300); };
  if (loading) return <div className="loading"><span/><p>Открываем учебную карту…</p></div>;
  if (!index?.loaded) return <Page title="Учебные треки" subtitle="Не удалось подключить исходный каталог Eidos."><div className="panel empty-learning">Проверьте папку learning_tracker рядом с приложением.</div></Page>;
  const nextTask = detail?.topic.tasks.find(task => !task.done);
  return <div className="learning-page">
    <header><div><div className="eyebrow">LEARNING WORKSPACE · {index.tracks.reduce((sum,item)=>sum+item.topics.length,0)} ТЕМ</div><h1>Стек знаний</h1><p>Открывай тему, понимай цель и сразу переходи к следующему действию.</p></div><button className="ghost prompt-lab-launch" onClick={() => window.pywebview?.api?.open_prompt_lab?.(selectedTrack, selectedTopic)}><Sparkles/> Prompt Lab</button></header>
    <div className="track-tabs">{index.tracks.map(item => <button key={item.id} className={item.id===selectedTrack?"active":""} onClick={()=>chooseTrack(item.id)} style={{"--track":item.color} as React.CSSProperties}><span>{item.id.toUpperCase()}</span><b>{item.title}</b><small>{item.done}/{item.total}</small></button>)}</div>
    <div className="learning-layout">
      <section className="topic-rail panel"><div className="topic-rail-head"><Layers3/><div><b>{track?.title}</b><span>{track?.topics.length} тем</span></div></div><div className="topic-list">{track?.topics.map(topic => <button key={topic.id} className={topic.id===selectedTopic?"active":""} onClick={()=>setSelectedTopic(topic.id)}><span>{String(topic.number).padStart(2,"0")}</span><div><b>{topic.title}</b><small>{topic.done}/{topic.total} заданий</small></div>{topic.done===topic.total&&topic.total>0?<Check/>:<ChevronRight/>}</button>)}</div></section>
      <section className="topic-detail panel">{!detail ? <div className="topic-loading"><span/><p>Загружаем тему…</p></div> : <>
        <div className="topic-hero" style={{"--track":detail.track.color} as React.CSSProperties}><div className="topic-count">ТЕМА {String(detail.topic.number).padStart(2,"0")}</div><h2>{detail.topic.title}</h2><p>{detail.topic.theory}</p><div className="topic-actions"><button onClick={()=>window.pywebview?.api?.open_prompt_lab?.(detail.track.id,detail.topic.id)}><Sparkles/> Изучить с наставником</button><button className="subtle" onClick={()=>void copy(nextTask?.statement || detail.topic.theory,"next")}>{copied==="next"?<Check/>:<Copy/>} {copied==="next"?"Скопировано":"Скопировать следующий шаг"}</button></div></div>
        <div className="topic-content">
          <div className="next-action"><div><span>СЛЕДУЮЩЕЕ ДЕЙСТВИЕ</span><h3>{nextTask?.title || "Все задания темы выполнены"}</h3><p>{nextTask?.statement || detail.topic.mastery}</p></div>{nextTask&&<strong><Clock3/>{nextTask.minutes} мин</strong>}</div>
          <div className="knowledge-grid"><article><span>Результат темы</span><p>{detail.topic.mastery}</p></article><article className="warning"><span><AlertTriangle/> Типичная ошибка</span><p>{detail.topic.pitfall}</p></article></div>
          <div className="task-section"><div className="section-label"><b>Задания</b><span>{detail.topic.tasks.filter(x=>x.done).length} из {detail.topic.tasks.length}</span></div>{detail.topic.tasks.map(task=><article className={`task-item ${task.done?"done":""}`} key={task.id}><div className="task-status">{task.done?<Check/>:task.label.slice(0,1)}</div><div><div className="task-meta"><span>{task.label}</span><i>{task.difficulty}</i><em>{task.minutes} мин</em></div><h3>{task.title}</h3><p>{task.statement}</p>{task.deliverable&&<small><b>Результат:</b> {task.deliverable}</small>}{task.external_url&&<a href={task.external_url} target="_blank" rel="noreferrer">Открыть материал <ExternalLink/></a>}</div></article>)}</div>
        </div>
      </>}</section>
    </div>
  </div>;
}

function PromptLab() {
  const params = new URLSearchParams(window.location.search);
  const [index, setIndex] = useState<LearningIndex | null>(null);
  const [trackId, setTrackId] = useState(params.get("track") || "");
  const [topicId, setTopicId] = useState(params.get("topic") || "");
  const [detail, setDetail] = useState<TopicDetail | null>(null);
  const [copied, setCopied] = useState("");
  useEffect(() => { document.body.classList.add("prompt-mode"); api.learning().then(value=>{setIndex(value); const track=value.tracks.find(x=>x.id===trackId)||value.tracks[0]; setTrackId(track?.id||""); setTopicId(current=>track?.topics.some(x=>x.id===current)?current:(track?.topics[0]?.id||""));}); return()=>document.body.classList.remove("prompt-mode"); }, []);
  useEffect(()=>{if(trackId&&topicId){setDetail(null);api.topic(trackId,topicId).then(setDetail)}},[trackId,topicId]);
  const track=index?.tracks.find(x=>x.id===trackId);
  const chooseTrack=(id:string)=>{const next=index?.tracks.find(x=>x.id===id);setTrackId(id);setTopicId(next?.topics[0]?.id||"")};
  const copy=async(text:string,key:string)=>{await navigator.clipboard.writeText(text);setCopied(key);window.setTimeout(()=>setCopied(""),1400)};
  return <div className="prompt-lab"><div className="prompt-titlebar"><div><Sparkles/><span>PROMPT LAB</span></div><button onClick={()=>window.pywebview?.api?.hide_prompt_lab?.()}><X/></button></div><header><div><div className="eyebrow">Отдельное пространство для AI-наставника</div><h1>Промпты для обучения</h1><p>Выбери тему, скопируй сценарий и открой новый чат без лишнего шума.</p></div></header>
    <div className="prompt-selectors"><label>Стек<select value={trackId} onChange={e=>chooseTrack(e.target.value)}>{index?.tracks.map(x=><option key={x.id} value={x.id}>{x.title}</option>)}</select></label><label>Тема<select value={topicId} onChange={e=>setTopicId(e.target.value)}>{track?.topics.map(x=><option key={x.id} value={x.id}>{String(x.number).padStart(2,"0")} · {x.title}</option>)}</select></label></div>
    {!detail?<div className="topic-loading"><span/><p>Готовим промпт…</p></div>:<div className="prompt-cards"><article><div className="prompt-card-head"><div><span>НАСТАВНИК</span><h2>{detail.topic.title}</h2></div><button onClick={()=>void copy(detail.topic.mentor_prompt,"mentor")}>{copied==="mentor"?<Check/>:<Copy/>}{copied==="mentor"?"Скопировано":"Копировать"}</button></div><p>{detail.topic.mentor_prompt}</p></article>{detail.topic.exam&&<article className="exam-prompt"><div className="prompt-card-head"><div><span>ЭКЗАМЕН · {detail.topic.exam.minutes} МИН</span><h2>{detail.topic.exam.title}</h2></div><button onClick={()=>void copy(detail.topic.exam!.exam_prompt,"exam")}>{copied==="exam"?<Check/>:<Copy/>}{copied==="exam"?"Скопировано":"Копировать"}</button></div><p>{detail.topic.exam.exam_prompt}</p></article>}</div>}
  </div>;
}

function PomodoroWidget() {
  const [timer, setTimer] = useState<TimerState>({ duration: 3000, remaining: 3000, running: false, task: "Фокус", mode: "focus" });
  const [settings,setSettings]=useState<PomodoroSettings>({focus_minutes:60,break_minutes:10,ambient_sound:"none",ambient_volume:35,auto_start_break:true});
  useEffect(() => {
    document.body.classList.add("widget-mode");
    let alive = true;
    const update = () => api.timer().then(value => alive && setTimer(value)).catch(() => {});
    void update();
    const poll = window.setInterval(update, 400);
    const updateSettings=()=>api.pomodoro().then(value=>alive&&setSettings(value)).catch(()=>{});
    void updateSettings();const settingsPoll=window.setInterval(updateSettings,1600);
    return () => { alive = false; window.clearInterval(poll);window.clearInterval(settingsPoll); document.body.classList.remove("widget-mode"); };
  }, []);
  const act = async (action: "start" | "pause" | "reset" | "complete") => setTimer(await api.timerAction(action, timer.task));
  const progress = Math.max(0, Math.min(1, 1 - timer.remaining / Math.max(1, timer.duration)));
  return <div className={`pomodoro-widget sound-${settings.ambient_sound} ${timer.running&&timer.mode==="focus"?"ambience-active":""}`}>
    {settings.ambient_sound!=="none"&&<div className="ambient-orbs" aria-hidden="true"><i/><i/><i/><i/></div>}
    <div className="widget-glow"/>
    <div className="widget-head"><span><i/> EIDOS FOCUS</span><button onClick={() => window.pywebview?.api?.hide_widget?.()}>×</button></div>
    <div className="widget-body">
      <div className="widget-ring" style={{"--widget-progress": `${progress * 360}deg`} as React.CSSProperties}><div><strong>{fmt(timer.remaining)}</strong><small>{timer.mode==="break"?"перерыв":timer.running?"в фокусе":"пауза"}</small></div></div>
      <div className="widget-copy"><span>{timer.mode==="break"?"Время восстановиться":"Сейчас главное"}</span><h2>{timer.mode==="break"?"Отойди от экрана и выдохни":timer.task||"Выбери задачу в Eidos"}</h2><div className="widget-controls"><button className="widget-play" onClick={() => void act(timer.running ? "pause" : "start")}>{timer.running ? <CirclePause/> : <Play/>}{timer.running ? "Пауза" : "Продолжить"}</button><button title={timer.mode==="break"?"Завершить перерыв":"Завершить сессию"} onClick={() => void act("complete")}><Check/></button><button title="Открыть Eidos" onClick={() => window.pywebview?.api?.show_main?.()}><ArrowRight/></button></div></div>
    </div>
  </div>;
}

export default App;
