import { Link, useLocation } from "react-router-dom";
import styles from "./navbar.module.css"
import { Badge } from "primereact/badge"

function DropdownItem({ url, text, icon, onClick, value}) {
    const location = useLocation();
    const isActive = location.pathname === url;
    return (
        <li>
            <Link to={url} className={`${styles.dropdown_item_link} ${isActive ? styles.active : ""}`} onClick={onClick}>
                <i className={icon}/>
                <span>{text}</span>
                {value > 0 && (<Badge value={value} style={{ marginLeft: 'auto' }}/>)}
            </Link>
        </li>
    )
}

export default DropdownItem;