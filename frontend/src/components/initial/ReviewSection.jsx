const ReviewSection = () => {
    return (
        <section id="reviews" className="reviews">


          <div className="container">


            <div className="section-title">

              <span>
                Отзывы
              </span>


              <h2>
                Что говорят наши студенты
              </h2>


            </div>




            <div className="reviews-grid">


              <div className="review">

                <p>
                  "После курса я смог собрать
                  свой первый полноценный backend
                  проект на Django."
                </p>


                <strong>
                  Алексей
                </strong>


              </div>



              <div className="review">

                <p>
                  "Понравился подход через практику.
                  Теория сразу превращается в код."
                </p>


                <strong>
                  Мария
                </strong>


              </div>



              <div className="review">

                <p>
                  "Хорошая структура обучения.
                  Понятно, куда двигаться дальше."
                </p>


                <strong>
                  Дмитрий
                </strong>


              </div>



            </div>


          </div>


        </section>
    )
}

export default ReviewSection