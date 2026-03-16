import { Link } from "react-router-dom";

function NavbarItem({ url, text}) {
    return (
        <li>
            <Link to={url}>
                {text}
            </Link>
        </li>
    )
}

export default NavbarItem