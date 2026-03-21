import "./navbar.css";
import logo from "../../assets/CIH_long_logo.png";
import pfp_placeholder from "../../assets/CIH_logo.jpg";
import { Link } from "react-router-dom";
import NavbarItem from "./NavbarItem";
import { PiSignOutFill } from "react-icons/pi";
import { FiSidebar } from "react-icons/fi";


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
                {/* Add navbar items here, specifying the url and the text you want displayed on the navbar */}
                <NavbarItem url="/files" text="Files"/>
                <NavbarItem url="/scans" text="Scans"/>
                <NavbarItem url="/roles" text="Roles"/>
            </ul>
        </div>
        {/* future use with accounts and potentially settings */}
        <div className="navbar-bottom">
            <div className="navbar-user">
                <div className="navbar-profile-picture">
                <img src={pfp_placeholder} alt="Profile picture" />
                </div>

                <div className="navbar-user-info">
                    <p className="navbar-user-name">John Doe</p>
                    {/* not used for now -- too cramped */}
                    {/* <p className="navbar-user-organisation">Cyber Innovation</p> */}
                </div>
            </div>
            <PiSignOutFill size={18} className="navbar-logout-button"/>
        </div>
    </div>
  );
}
export default Navbar;