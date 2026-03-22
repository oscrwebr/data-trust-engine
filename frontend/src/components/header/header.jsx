import styles from "./header.module.css"
import { FiSidebar } from "react-icons/fi";

import { Button } from "primereact/button";
function Header({firstname, lastname, workspace, sidebarVisible, setSidebarVisible}){
    return(
        <div className={styles.container}>
            <div className={styles.header}>
                <div className={styles.topRow}>
                    <div className={styles.sidebar_icon_text}>
                        {!sidebarVisible &&(<FiSidebar onClick={() => setSidebarVisible(true)} className={styles.sidebar_toggle_icon} size={20} color="black"/>)}
                        <span>{firstname} {lastname} / <span className={styles.workspace_text}>{workspace}</span></span>
                    </div>             
                    <Button 
                        data-testid="notification-button"
                        className={styles.notification_button}
                        text 
                        style={{marginRight: 30, background: "transparent", border: "none", boxShadow: "none", outline: "none"}}>
                            <i data-testid="badge" className="pi pi-bell p-overlay-badge" style={{ fontSize: 21}}></i>
                    </Button>
                </div>
                <div className={styles.line}/>
            </div>
        </div>
    )
}

export default Header;