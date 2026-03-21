import { FiSidebar } from "react-icons/fi";
import { Link } from "react-router-dom";

import logo from "../../assets/CIH_long_logo.png";
import styles from "./navbar.module.css"

function AdminNavbar({setSidebarVisible}){

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
            <div className={styles.actions_container}>
                
            </div>

            <div className={styles.workspace_container}>

            </div>
        </div>
    )
}

export default AdminNavbar;