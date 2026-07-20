import "../styles/Courses.css";
import Header from "../components/initial/Header"
import Footer from "../components/initial/Footer"
import CoursesHero from "../components/courses_list/CoursesHero";
import CoursesFilter from "../components/courses_list/CoursesFilter";
import CoursesList from "../components/courses_list/CoursesList";
import { useState } from "react";

function Courses() {
  const [activeFilter, setActiveFilter] = useState("All");
  const [search, setSearch] = useState("");
  return (
    <div className="courses-page">
      <main>
        <CoursesHero search={search} setSearch={setSearch} />

        <CoursesFilter activeFilter={activeFilter} setActiveFilter={setActiveFilter}/>

        <CoursesList activeFilter={activeFilter} search={search} setSearch={setSearch}/>
      </main>
    </div>
  );
}

export default Courses;
