import CourseCard from "./CourseCard"

const Courses = () => {
  const courses = [
  {
    id: 1,
    title: "Python",
    description: "...",
    icon: "PY",
  },
  {
    id: 2,
    title: "Django",
    description: "...",
    icon: "DJ",
  },
  {
    id: 3,
    title: "React",
    description: "...",
    icon: "JS",
  },
];

       return (
        <section id="courses" className="courses">

          <div className="container">


            <div className="section-title">

              <span>
                Направления
              </span>


              <h2>
                Выбери свою технологию
              </h2>


            </div>



            <div className="course-grid">
            
            {courses.map((course) => (< CourseCard key={course.id} title={course.title} description={course.description} icon={course.icon} />))}
            </div>


          </div>


        </section>

    )
}

export default Courses