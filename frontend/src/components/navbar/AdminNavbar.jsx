import { FiSidebar } from "react-icons/fi";
import { Link } from "react-router-dom";

import logo from "../../assets/CIH_long_logo.png";
import styles from "./navbar.module.css"
import SidebarDropdown from "../dropdown/SidebarDropdown";
import NavbarItem from "./NavbarItem";

function AdminNavbar({setSidebarVisible, firstname, surname}){

    return(
        <div className={styles.container}>
            <div className={styles.header_container}>
                <Link>
                    <div className={styles.navbar_logo}>
                        <img src={logo} alt="CIH Logo"/>
                    </div>
                </Link>
                <FiSidebar onClick={() => setSidebarVisible(false)} className={styles.sidebar_toggle_icon} size={27} color="#fff"/>
            </div>
            <div className={styles.line}/>
            <div>
                <span>Workspace</span>
                <NavbarItem url="/dashboard" text="Dashboard" icon="pi pi-th-large"/>

                <SidebarDropdown icon="pi pi-folder" label="Scanning">
                    {/* Add your scanning pages here */}
                </SidebarDropdown>

                <SidebarDropdown icon="pi pi-users" label="My Employees">
                    <NavbarItem url="/view-employees" text="View Employees"/>
                    <NavbarItem url="/manage-employees" text="Manage Employees"/>
                    <NavbarItem url="/send-invites" text="Send Invite"/>
                </SidebarDropdown>

                <SidebarDropdown icon="pi pi-pen-to-square" label="Configure">
                    <NavbarItem url="/roles" text="Create Roles"/>
                    <NavbarItem url="/upload-org-chart" text="Upload Org Chart"/>
                </SidebarDropdown>

                <NavbarItem url="/settings" text="Settings" icon="pi pi-cog"/>
                <NavbarItem text="Sign-out" icon="pi pi-sign-out"/>
            </div>
            <div className={styles.line}/>
            <div>
                <div>PFP goes here</div>
                <div>{firstname} {surname}</div>
            </div>
        </div>
    )
}

export default AdminNavbar;