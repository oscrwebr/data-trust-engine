import { Link } from "react-router-dom";
import "./navbar.css";

function NavbarItem({ url, text, icon }) {
    return (
        <li>
            <Link to={url} className="navbar-item">
                <span className="navbar-icon">{icon}</span>
                <span className="navbar-text">{text}</span>
            </Link>
        </li>
    );
}

export default NavbarItem