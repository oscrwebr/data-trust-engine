import { Link } from "react-router-dom";
import styles from "./navbar.module.css"
import { Badge } from "primereact/Badge"

function DropdownItem({ url, text, icon, onClick, value}) {
    return (
        <li>
            <Link to={url} className={styles.dropdown_item_link} onClick={onClick}>
                <i className={icon}/>
                <span>{text}</span>
                {value != null && <Badge value={value} style={{ marginLeft: 'auto' }}/>}
            </Link>
        </li>
    )
}

export default DropdownItem;