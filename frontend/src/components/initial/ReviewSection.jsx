import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../api/apiRequest";

export default function ReviewSection() {
  const [reviews, setReviews] = useState([]);
  useEffect(() => {
    let active = true;
    apiRequest("/api/feedback/", { auth: false }).then(async (response) => {
      if (!response.ok) return;
      const data = await response.json();
      if (active) setReviews((data.entries || []).filter((entry) => entry.kind === "review").slice(0, 3));
    }).catch(() => {});
    return () => { active = false; };
  }, []);
  return <section id="reviews" className="reviews"><div className="container">
    <div className="section-title"><span>Обратная связь</span><h2>Впечатления учеников</h2></div>
    {reviews.length > 0 ? <div className="reviews-grid">{reviews.map((review) =>
      <article className="review" key={review.id}><p style={{ overflowWrap: "anywhere", whiteSpace: "pre-wrap" }}>{review.message.length > 220 ? `${review.message.slice(0, 220)}…` : review.message}</p><strong>{review.author}</strong></article>
    )}</div> : <p>Уже попробовали учиться? Поделитесь впечатлением — это поможет улучшить курсы.</p>}
    <Link to="/feedback" className="community-write">Отзывы и вопросы →</Link>
  </div></section>;
}
