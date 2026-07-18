const FAQSection = () => {
    return (
        <section className="faq">


          <div className="container">


            <div className="section-title">

              <span>
                FAQ
              </span>

              <h2>
                Частые вопросы
              </h2>

            </div>



            <div className="faq-list">


              <div className="faq-item">

                <h3>
                  Нужно ли знать программирование?
                </h3>

                <p>
                  Нет. Курсы построены так,
                  чтобы постепенно перейти от основ
                  к созданию проектов.
                </p>

              </div>



              <div className="faq-item">

                <h3>
                  Можно ли учиться самостоятельно?
                </h3>

                <p>
                  Да. Все материалы доступны онлайн,
                  а обучение построено вокруг практики.
                </p>

              </div>



              <div className="faq-item">

                <h3>
                  Будут ли реальные проекты?
                </h3>

                <p>
                  Да. Главная цель — создать
                  полноценное портфолио.
                </p>

              </div>


            </div>


          </div>


        </section>
    )
}

export default FAQSection