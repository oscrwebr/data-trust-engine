import { Link } from "react-router-dom";

function NavbarItem({ url, text, icon}) {
    return (
        <li>
            <Link to={url}>
                <i className={icon}/>
                {text}
            </Link>
        </li>
    )
}

export default NavbarItem