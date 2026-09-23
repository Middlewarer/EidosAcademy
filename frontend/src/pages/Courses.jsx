import "../styles/Courses.css";
import Header from "../components/initial/Header"
import Footer from "../components/initial/Footer"
import CoursesHero from "../components/courses_list/CoursesHero";
import CoursesFilter from "../components/courses_list/CoursesFilter";
import CoursesList from "../components/courses_list/CoursesList";
import { useState } from "react";
import Crumbs from "../components/Crumbs";
import { useFavorites } from "../components/context/FavoritesContext";

function Courses({ favoritesOnly = false }) {
  const { ids, clear } = useFavorites();
  const [activeFilter, setActiveFilter] = useState("All");
  const [search, setSearch] = useState("");
  return (
    <div className="courses-page">
      <main>
        <Crumbs items={[{ label: favoritesOnly ? "Избранные курсы" : "Курсы" }]} />
        {favoritesOnly ? <section className="container learning-intro"><h1>Избранные курсы</h1>
          <p>Сохраните интересные направления и возвращайтесь, когда будете готовы учиться. Список хранится в этом браузере.</p>
          {ids.length > 0 && <p><button className="learning-button" onClick={clear}>Очистить избранное ({ids.length})</button></p>}
          <label>Поиск в избранном <input className="learning-input" value={search} onChange={(event) => setSearch(event.target.value)} type="search" /></label>
        </section> : <CoursesHero search={search} setSearch={setSearch} />}

        <CoursesFilter activeFilter={activeFilter} setActiveFilter={setActiveFilter}/>

        <CoursesList activeFilter={activeFilter} search={search} favoritesOnly={favoritesOnly}/>
      </main>
    </div>
  );
}

export default Courses;
