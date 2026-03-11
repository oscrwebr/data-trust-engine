import "./navbar.css";
import logo from "../../assets/CIH_long_logo.png";
import { Link } from "react-router-dom";
import NavbarItem from "./NavbarItem";

function Navbar() {

  return (
    <div className="navbar-base">
        {/* "/" placeholder for whatever page ends up being home/main page */}
        <Link to="/">
            <div className="navbar-logo">
                <img src={logo} alt="CIH Logo"/>
            </div>
        </Link>
        <div className="navbar-list">
            <ul className="navbar-items">
                <NavbarItem url="/files" text="Files"/>
                <NavbarItem url="/scans" text="Scans"/>
            </ul>
        </div>
    </div>
  );
}
export default Navbar;