import { FiSidebar } from "react-icons/fi";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import logo from "../../assets/CIH_long_logo.png";
import styles from "./navbar.module.css"
import SidebarDropdown from "../dropdown/dropdown";
import NavbarItem from "./NavbarItem";
import DropdownItem from "./DropdownItem";
import api from "../../api/axiosConfig";
import { Avatar } from "primereact/Avatar";
        
function Sidebar({setSidebarVisible, firstname, surname, email, setVisible, role}){
    const [openDropdown, setOpenDropdown] = useState(null);
    const [pendingEmployees, setPendingEmployees] = useState([])
    const [workspace_id, setWorkspaceId] = useState(null)
    const user_initials = (firstname?.[0]?.toUpperCase() || "?") + (surname?.[0]?.toUpperCase() || "?");

    useEffect(() => {
        api.get("/workspace/dashboard")
        .then(res => {
            setWorkspaceId(res.data.id)
            console.log(res.data.id)
        })

        api.get("/workspace/get-pending-employees")
        .then(res => {
            setPendingEmployees(res.data)
        })
    }, []);

    return(
        <div className={styles.container}>
        {role === "admin" ? (
            <>
                <div className={styles.header_container}>
                    <Link to="/">
                        <div className={styles.navbar_logo}>
                            <img src={logo} alt="CIH Logo"/>
                        </div>
                    </Link>

                    {/* Close sidebar icon */}
                    <FiSidebar data-testid="close-button" onClick={() => setSidebarVisible(false)} className={styles.sidebar_toggle_icon}/>
                </div>
                <div className={styles.line}/>
                <div className={styles.navbar_content}>
                    <div className={styles.user_role_container}>
                        <span className={styles.navbar_title}>Workspace</span>
                        <span className={styles.user_role_card}>Admin</span>
                    </div>
                    <NavbarItem className={styles.navbar_item} url="/dashboard" text="Dashboard" icon="pi pi-th-large"/>
                    <div className={styles.line}/>

                    {/* Add a dropdown menu item using SidebarDropdown - choose your own label, an icon from PrimeReact and everything else can be kept the same*/}
                    <SidebarDropdown className={styles.dropdown} icon="pi pi-folder" label="Scanning" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown}>

                        {/* Add your scanning pages here */}
                    </SidebarDropdown>

                    <SidebarDropdown data-testid="my-employees-element" className={styles.dropdown} icon="pi pi-users" label="My Employees" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown}>

                        {/* SidebarDropdowns have their own children for styling purposes - specify the url and text displayed */}
                        <DropdownItem url="/view-employees" text="View Employees"/>
                        <DropdownItem url="/manage-employees" text="Manage Employees" value={pendingEmployees.length}/>
                        <DropdownItem onClick={() => setVisible(true)} text="Send Invite"/>
                    </SidebarDropdown>

                    <SidebarDropdown className={styles.dropdown} icon="pi pi-pen-to-square" label="Configure" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown}>
                        <DropdownItem url="/roles" text="Create Roles"/>
                        <DropdownItem url="/upload-org-chart" text="Upload Org Chart"/>
                    </SidebarDropdown>

                    <div className={styles.line}/>

                    {/* Add regular navbar items here, specifying the url and the text you want displayed on the navbar */}
                    <NavbarItem url="/settings" text="Settings" icon="pi pi-cog"/>
                    <NavbarItem text="Sign-out" icon="pi pi-sign-out"/>
                    <div className={styles.line}/>
                </div> 
                <div className={styles.user_info_container}>
                    <img className={styles.user_logo} src={`http://localhost:8000/workspace/image/${workspace_id}`} alt="Workspace Logo"/>
                    <div>
                        <div className={styles.user_name}>{firstname} {surname}</div>
                        <div className={styles.user_email}>{email}</div>
                    </div>
                </div>
            </>
        ) : (
            <>
                <div className={styles.header_container}>
                    <Link to="/">
                        <div className={styles.navbar_logo}>
                            <img src={logo} alt="CIH Logo"/>
                        </div>
                    </Link>

                    {/* Close sidebar icon */}
                    <FiSidebar data-testid="close-button" onClick={() => setSidebarVisible(false)} className={styles.sidebar_toggle_icon} size={27} color="#fff"/>
                </div>
                <div className={styles.line}/>
                <div className={styles.navbar_content}>
                    <div className={styles.user_role_container}>
                        <span className={styles.navbar_title}>Workspace</span>
                        <span className={styles.user_role_card}>Employee</span>
                    </div>

                    {/* Add regular navbar items like this, specifying the url and the text you want displayed on the navbar */}
                    <NavbarItem className={styles.navbar_item} url="/dashboard" text="Dashboard" icon="pi pi-th-large"/>
                    <div className={styles.line}/>
                    <NavbarItem url="/settings" text="Settings" icon="pi pi-cog"/>
                    <NavbarItem text="Sign-out" icon="pi pi-sign-out"/>
                    <div className={styles.line}/>
                </div> 
                <div className={styles.user_info_container}>
                    <Avatar label={user_initials} size="large" shape="circle" />
                    <div>
                        <div className={styles.user_name}>{firstname} {surname}</div>
                        <div className={styles.user_email}>{email}</div>
                    </div>
                </div>
            </>
        )}
        </div>
    )
}

export default Sidebar;