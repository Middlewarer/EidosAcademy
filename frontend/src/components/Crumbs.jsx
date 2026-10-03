import { Link } from "react-router-dom";

const Crumbs = ({ items = [] }) => {
    return (
        <nav className="learning-crumbs container" aria-label="Хлебные крошки">
          <ol>
            {items.map((item, index) => <li key={`${item.label}-${index}`}>
              {item.to ? <Link to={item.to}>{item.label}</Link> : <span aria-current="page">{item.label}</span>}
            </li>)}
          </ol>
        </nav>
    )
}

export default Crumbs;
