const Module = (props) => {
    const {
        title,
        topics,
    } = props
    return (<article className="course-detail-module">
                <h3>{title}</h3>

                <ul>
                  {topics.map((topic, index) => (
    <li key={index}>{topic.title}</li>
))}
                </ul>
              </article>)
}

export default Module