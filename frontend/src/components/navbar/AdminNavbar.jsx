import { FiSidebar } from "react-icons/fi";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import logo from "../../assets/CIH_long_logo.png";
import styles from "./navbar.module.css"
import SidebarDropdown from "../dropdown/dropdown";
import NavbarItem from "./NavbarItem";
import DropdownItem from "./DropdownItem";
import api from "../../api/axiosConfig";
        
function AdminNavbar({setSidebarVisible, firstname, surname, setVisible}){
    const [openDropdown, setOpenDropdown] = useState(null);
    const [imageSrc, setImageSrc] = useState("");

    useEffect(() => {
        api.get("/workspace/get-workspace-image", {responseType: "blob"})
        .then(res => {
            const url = URL.createObjectURL(res.data);
            setImageSrc(url);
        });
    }, []);

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
            <div className={styles.navbar_content}>
                <div className={styles.user_role_container}>
                    <span className={styles.navbar_title}>Workspace</span>
                    <span className={styles.user_role_card}>Admin</span>
                </div>
                <NavbarItem className={styles.navbar_item} url="/dashboard" text="Dashboard" icon="pi pi-th-large"/>
                <div className={styles.line}/>
                <SidebarDropdown className={styles.dropdown} icon="pi pi-folder" label="Scanning" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown}>
                    {/* Add your scanning pages here */}
                </SidebarDropdown>
   
                <SidebarDropdown className={styles.dropdown} icon="pi pi-users" label="My Employees" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown}>
                    <DropdownItem url="/view-employees" text="View Employees"/>
                    <DropdownItem url="/manage-employees" text="Manage Employees"/>
                    <DropdownItem onClick={() => setVisible(true)} text="Send Invite"/>
                </SidebarDropdown>

                <SidebarDropdown className={styles.dropdown} icon="pi pi-pen-to-square" label="Configure" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown}>
                    <DropdownItem url="/roles" text="Create Roles"/>
                    <DropdownItem url="/upload-org-chart" text="Upload Org Chart"/>
                </SidebarDropdown>
                <div className={styles.line}/>
                <NavbarItem url="/settings" text="Settings" icon="pi pi-cog"/>
                <NavbarItem text="Sign-out" icon="pi pi-sign-out"/>
                <div className={styles.line}/>
            </div> 
            <div className={styles.user_info_container}>
                <img className={styles.user_logo} src={imageSrc} alt="Workspace Logo"/>
                <div className={styles.user_name}>{firstname} {surname}</div>
            </div>
        </div>
    )
}

export default AdminNavbar;