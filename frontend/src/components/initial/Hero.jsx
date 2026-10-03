import { Link } from "react-router-dom"

function Hero() {
    return (
        <section className="hero">

          <div className="container hero-content">


            <div className="hero-text">


              <div className="badge">
                💡 EidosAcademy — учимся шаг за шагом
              </div>


              <h1>
                Превращай идеи
                <br />
                в реальные технологии
              </h1>


              <p>
                Практические курсы по программированию,
                разработке приложений и созданию цифровых
                продуктов с нуля.
              </p>


              <div className="hero-buttons">

              <Link to="/courses" className="primary-btn">Выбрать курс</Link>

              <Link to="/feedback" className="secondary-btn">Задать вопрос</Link>

              </div>


              <div className="hero-info">
                <div><strong>В своём темпе</strong>без расписания</div>
                <div><strong>По темам</strong>понятная программа</div>
                <div><strong>С прогрессом</strong>продолжайте с места остановки</div>
              </div>


            </div>



            <div className="hero-visual">


              <div className="light-circle"></div>


              <div className="lamp-card">

                <div className="lamp">
                  💡
                </div>


                <h3>
                  Идея — навык — профессия
                </h3>


                <p>
                  Учись создавать продукты,
                  которые имеют ценность.
                </p>

              </div>


              <div className="floating-card python">
                Python
              </div>


              <div className="floating-card django">
                Django
              </div>


              <div className="floating-card react">
                React
              </div>


            </div>


          </div>

        </section>
    )
}

export default Hero
