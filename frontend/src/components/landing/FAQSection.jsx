import FAQItem from "./FAQItem"

const FAQSection = () => {

    const questions = [
      {question: "Подходит ли обучение новичкам?",
       answer: "Да. Курсы рассчитаны на студентов без опыта программирования. \
       Мы начинаем с фундаментальных понятий и постепенно переходим к созданию реальных проектов."
      },
      {question: "Как проходит обучение?",
        answer: "Каждый курс состоит из теоретических уроков, практических заданий и проектов. \
        Основной упор делается на разработку приложений, а не на изучение теории в отрыве от практики."
      },
      {
        question: "Будут ли домашние задания?",
        answer: "Да. После каждого модуля предусмотрены практические задания. Они помогают закрепить материал и сформировать портфолио."
      }
    ]

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


              {questions.map((instance) => (
                <FAQItem 
              key={instance.question}
              question={instance.question}
              answer={instance.answer}
              />
            ))}
              
              

            </div>


          </div>


        </section>
    )
}

export default FAQSection