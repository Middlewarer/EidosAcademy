import CourseCard from "./CourseCard"

const Courses = () => {
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


              < CourseCard title="Django" description="Научитесь создавать джанго приложения за 15 минут"/>
              < CourseCard title="Python" description="Что же делать? Конечно же учить Python!" />
              < CourseCard title="REST API" description="Научитесь передавать данные от сервера к рабочему клиенту в этом курсе!" />



            </div>


          </div>


        </section>

    )
}

export default Courses