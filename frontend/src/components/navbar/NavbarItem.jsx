import { Link } from "react-router-dom";
import styles from "./navbar.module.css"

function NavbarItem({ url, text, icon, onClick}) {
    return (
        <li>
            <Link to={url} className={styles.navbar_link} onClick={onClick}>
                <i className={icon}/>
                <span>{text}</span>
            </Link>
        </li>
    );
}

export default NavbarItem