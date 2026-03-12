import "./navbar.css";
import logo from "../../assets/CIH_long_logo.png";
import pfp_placeholder from "../../assets/CIH_logo.jpg";
import { Link } from "react-router-dom";
import NavbarItem from "./NavbarItem";
import { PiGear } from "react-icons/pi";
import { PiUserCircleLight } from "react-icons/pi";
import { PiSignOutFill } from "react-icons/pi";
import { PiScan } from "react-icons/pi";
import { PiFolder } from "react-icons/pi";
import { PiMapTrifold } from "react-icons/pi";
import { PiUsersThree } from "react-icons/pi";
import { PiDiamondsFourLight } from "react-icons/pi";

function Navbar() {

  return (
    <div className="navbar-base">
        {/* "/" placeholder for whatever page ends up being home/main page */}
        <Link to="/dashboard">
            <div className="navbar-logo">
                <img src={logo} alt="CIH Logo"/>
            </div>
        </Link>
        <div className="navbar-list">
            <ul className="navbar-items">
                {/* Add navbar items here, specifying the URL, text and icon you want displayed on the navbar */}
                <NavbarItem url="/dashboard" text="Dashboard" icon={<PiDiamondsFourLight/>}/>
                <NavbarItem url="/files" text="Files" icon={<PiFolder/>}/>
                <NavbarItem url="/scans" text="Scans" icon={<PiScan/>}/>
                <NavbarItem url="/access-map" text="Access Map" icon={<PiMapTrifold/>}/>
                <NavbarItem url="/roles" text="Roles" icon={<PiUsersThree/>}/>

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