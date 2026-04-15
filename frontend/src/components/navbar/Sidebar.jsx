import { FiSidebar } from "react-icons/fi";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import logo from "../../assets/CIH_long_logo.png";
import styles from "./navbar.module.css"
import SidebarDropdown from "../dropdown/dropdown";
import DropdownItem from "./DropdownItem";
import DropdownItemNoLink from "./DropdownItemNoLink.jsx";
import api from "../../api/axiosConfig";
import { Avatar } from "primereact/avatar";
import { setAccessToken, getAccessToken } from "../../Auth/authStore.js";
import { BiFileFind } from "react-icons/bi";
        
function Sidebar({setSidebarVisible, firstname, surname, email, setVisible, role}){
    const [openDropdown, setOpenDropdown] = useState(null);
    const [pendingEmployees, setPendingEmployees] = useState([]);
    const [workspace_id, setWorkspaceId] = useState(null);
    const backend_uri = import.meta.env.VITE_BACKEND_HOST || "http://localhost:8000"
    const user_initials = (firstname?.[0]?.toUpperCase() || "?") + (surname?.[0]?.toUpperCase() || "?");
    const nav = useNavigate();

    useEffect(() => {
        api.get("/workspace/dashboard")
        .then(res => {
            setWorkspaceId(res.data.id)
        })

        api.get("/workspace/get-pending-employees")
        .then(res => {
            setPendingEmployees(res.data)
        })
    }, []);

    async function signOut() {
        console.log(`This is the access token before removal${getAccessToken()}`);
        // Hitting the signout endpoint to remove refresh token 
        let logoutStatus = 400
        await api.post("/auth/logout")
        .then(res => {
            logoutStatus = res.status
        })
        .catch(err => {
        });
        // Clearing the access token from local memory
        setAccessToken(null);
        // redirecting user to the homepage
        nav("/", {state: {status_code: logoutStatus}})
    }

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
                    <DropdownItem className={styles.navbar_item} url="/dashboard" text="Dashboard" icon="pi pi-th-large"/>
                    <div className={styles.line}/>
                    <SidebarDropdown className={styles.dropdown} icon="pi pi-file" label="Files" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown}>
                       <DropdownItem url="/dashboard-files" text="View Files"/>

                    </SidebarDropdown>
                    {/* Add a dropdown menu item using SidebarDropdown - choose your own label, an icon from PrimeReact and everything else can be kept the same*/}
                    <SidebarDropdown className={styles.dropdown} icon="pi pi-search" label="Scanning" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown} basePaths={["/files"]}>
                        {/* Add your scanning pages here */}
                        {/* Make sure to add the paths of these scanning pages to the basePaths array inside SidebarDropdown props*/}
                        <DropdownItem url="/scans" text="View Scans"/>
                    </SidebarDropdown>

                    <SidebarDropdown data-testid="my-employees-element" className={styles.dropdown} icon="pi pi-users" label="My Employees" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown} basePaths={["/view-employees", "/manage-employees"]}>

                        {/* SidebarDropdowns have their own children for styling purposes - specify the url and text displayed */}
                        <DropdownItem url="/view-employees" text="View Employees"/>
                        <DropdownItem url="/manage-employees" text="Manage Employees" value={pendingEmployees.length}/>
                    </SidebarDropdown>

                    <SidebarDropdown className={styles.dropdown} icon="pi pi-pen-to-square" label="Configure" openDropdown={openDropdown} setOpenDropdown={setOpenDropdown} basePaths={["/roles", "/upload-org-chart"]}>
                        <DropdownItem url="/roles" text="Create Roles"/>
                        <DropdownItem url="/upload-org-chart" text="Upload Org Chart"/>
                    </SidebarDropdown>

                    <div className={styles.line}/>

                    {/* Add regular navbar items here, specifying the url and the text you want displayed on the navbar */}
                    <DropdownItem url="/settings" text="Settings" icon="pi pi-cog"/>
                    <DropdownItemNoLink onClick={() => signOut()} text="Sign-out" icon="pi pi-sign-out"/>
                    <div className={styles.line}/>
                </div> 
                <div className={styles.user_info_container}>
                    <img className={styles.user_logo} src={`${backend_uri}/workspace/image/${workspace_id}`} alt="Workspace Logo"/>
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
                    <DropdownItem className={styles.navbar_item} url="/dashboard" text="Dashboard" icon="pi pi-th-large"/>
                    <div className={styles.line}/>
                    <DropdownItem url="/settings" text="Settings" icon="pi pi-cog"/>
                    <DropdownItemNoLink onClick={() => signOut()} text="Sign-out" icon="pi pi-sign-out"/>
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