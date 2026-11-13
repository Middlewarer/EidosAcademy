import { Link } from "react-router-dom"
import { useState } from "react";
import FavoriteButton from "./FavoriteButton";
import CoursePreview from "./CoursePreview";

const CourseCard = ({ title, description, image, id }) => {
    const [preview, setPreview] = useState(false);
    return (
        <article className="group flex min-h-[360px] flex-col overflow-hidden rounded-3xl border border-[var(--line)] bg-[var(--white)] p-5 shadow-[0_10px_35px_rgba(34,46,80,.05)] transition duration-300 hover:-translate-y-1.5 hover:border-blue-300 hover:shadow-[0_22px_55px_rgba(34,46,80,.12)] sm:p-6">
        <Link
          to={`/courses/${id}`}
          className="flex flex-1 flex-col text-inherit no-underline"
          aria-label={`Открыть курс «${title}»`}
        >

            <div className="grid aspect-video w-full place-items-center overflow-hidden rounded-2xl bg-gradient-to-br from-blue-100 to-[var(--paper)] text-4xl font-extrabold text-[var(--blue)] dark:from-blue-950">
              {image ? <img className="h-full w-full object-cover transition duration-300 group-hover:scale-[1.03]" src={image} alt={`Обложка курса «${title}»`} loading="lazy" /> : <span aria-hidden="true">{title?.charAt(0)}</span>}
            </div>

            <h3 className="mt-5 text-xl font-extrabold tracking-tight text-[var(--ink)]">{title}</h3>

            <p className="mt-3 line-clamp-3 leading-6 text-[var(--muted)]">{description}</p>

        </Link>
        <div className="mt-6 flex flex-wrap gap-2 border-t border-[var(--line)] pt-4">
          <FavoriteButton id={id} />
          <button className="rounded-xl bg-[var(--blue)] px-4 py-2.5 text-sm font-bold text-white transition hover:-translate-y-0.5 hover:bg-[var(--blue-dark)]" type="button" onClick={() => setPreview(true)}>Быстрый просмотр</button>
        </div>
        {preview && <CoursePreview course={{ id, title, description }} onClose={() => setPreview(false)} />}
        </article>
    )
}

export default CourseCard
