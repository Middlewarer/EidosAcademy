const Courses = () => {
    return (
        <main className="courses-page">

            <section className="courses-hero">

                <div className="container">

                    <span className="section-label">
                        Каталог
                    </span>

                    <h1>
                        Найдите курс, который приблизит вас к первой работе
                    </h1>

                    <p>
                        Изучайте современные технологии разработки через практику,
                        реальные проекты и понятные объяснения.
                    </p>

                    <div className="search-box">

                        <input
                            type="text"
                            placeholder="Поиск курса..."
                        />

                        <button>
                            Найти
                        </button>

                    </div>

                </div>

            </section>


            <section className="course-filters">

                <div className="container">

                    <button>Все</button>
                    <button>Backend</button>
                    <button>Frontend</button>
                    <button>Python</button>
                    <button>React</button>
                    <button>Django</button>

                </div>

            </section>


            <section className="courses-list">

                <div className="container">

                    <div className="courses-grid">

                        {/* CourseCard */}

                    </div>

                </div>

            </section>

        </main>
    );
};

export default Courses;