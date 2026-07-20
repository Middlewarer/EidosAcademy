import { useEffect, useState } from "react"
import CourseCard from "../CourseCard"

const CoursesList = (props) => {
  const {activeFilter, search} = props

    const [courses, setCourses] = useState([])

    const getCourses = async () => {
        const response = await fetch("http://127.0.0.1:8000/api/courses/")
        const data = await response.json()
        
        setCourses(data.courses)
    }

     useEffect(() => {
      getCourses()
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
              (< CourseCard key={course.id}
              title={course.title}
              description={ course.description.length > 120 ? course.description.slice(0, 120) + "..." : course.description}/>))}
            </div>
          </div>
        </section>
    )
}

export default CoursesList