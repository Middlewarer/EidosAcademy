import { Link } from "react-router-dom";

const Crumbs = ({ items = [{ label: "Курсы", to: "/courses" }] }) => {
    return (
        <nav className="learning-crumbs container" aria-label="Хлебные крошки">
          <ol><li><Link to="/">Главная</Link></li>
            {items.map((item, index) => <li key={index}>
              {item.to ? <Link to={item.to}>{item.label}</Link> : <span aria-current="page">{item.label}</span>}
            </li>)}
          </ol>
        </nav>
    )
}

export default Crumbs;
