import { useEffect, useState } from "react"
import CourseCard from "../CourseCard"

import { getCourses } from "../api/courses/Courses.jsx"

const CoursesList = (props) => {
  const {activeFilter, search} = props

    const [courses, setCourses] = useState([])

    useEffect(() => {
      async function load() {
        try {
          const data = await getCourses();
          setCourses(data.courses)
        } catch (err) {
          console.log(err)
        }
      }

      load();
    }, []);

    const filteredCourses = courses.filter((course) => {
    if (activeFilter === "All") {
        return true;
    }
    return course.title.includes(activeFilter);
}).filter((course) => course.title.includes(search));

    

    return (
        <section className="courses-list">
          <div className="container">
            <p className="courses-count">Найдено курсов: {filteredCourses.length}</p>

            <div className="courses-grid">
              {filteredCourses.map((course) =>
              (<CourseCard
              key={course.id}
              id={course.id}
              title={course.title}
              description={ course.description.length > 120 ? course.description.slice(0, 120) + "..." : course.description} />))}
            </div>
          </div>
        </section>
    )
}

export default CoursesList