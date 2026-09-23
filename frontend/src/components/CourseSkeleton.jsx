export default function CourseSkeleton() {
  return <div className="course-skeleton" role="status" aria-label="Загрузка курса">
    <div className="course-skeleton__cover" />
    <div className="course-skeleton__line" /><div className="course-skeleton__line" />
    <div className="course-skeleton__line course-skeleton__line--short" />
  </div>;
}
