import { Link } from "react-router-dom";
import styles from "./navbar.module.css"

function DropdownItem({ url, text, icon, onClick}) {
    return (
        <li>
            <Link to={url} className={styles.dropdown_item_link} onClick={onClick}>
                <i className={icon}/>
                <span>{text}</span>
            </Link>
        </li>
    )
}

export default DropdownItem;