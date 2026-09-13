import FAQItem from "./FAQItem"

const FAQSection = () => {

    const questions = [
      {question: "Как выбрать курс?", answer: "Откройте описание и программу курса без регистрации. Посмотрите список тем и выберите подходящее направление."},
      {question: "Как сохраняется прогресс?", answer: "После входа мы запоминаем последнюю открытую тему. Когда закончите изучение материала, нажмите «Завершить тему». Это отметка о прохождении, а не проверка знаний."},
      {question: "Что делать, если материал непонятен или найдена ошибка?", answer: "Напишите на странице обратной связи. Укажите курс и тему, а для ошибки — ещё и шаги, после которых она возникает."}
    ];

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