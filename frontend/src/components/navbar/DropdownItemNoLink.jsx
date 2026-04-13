import { Link, useLocation } from "react-router-dom";
import styles from "./navbar.module.css"
import { Badge } from "primereact/badge"

function DropdownItemNoLink({ url, text, icon, onClick, value }) {
    const location = useLocation();
    const isActive = location.pathname === url;

    return (
        <li>
            <button  className={`${styles.dropdown_item_link} ${isActive ? styles.active : ""}`} onClick={onClick}>
                <i className={icon}/>
                <span>{text}</span>
                {value != null && <Badge value={value} style={{ marginLeft: 'auto' }}/>}
            </button>
        </li>
    )
}

export default DropdownItemNoLink;