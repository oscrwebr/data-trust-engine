import "primereact/resources/themes/lara-light-indigo/theme.css"; 
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";
import styles from "./header.module.css"

import { Button } from "primereact/button";
function Header({firstname, lastname, workspace}){
    return(
        <div className={styles.container}>
            <div className={styles.header}>
                <div className={styles.topRow}>
                    <span>{firstname} {lastname} / {workspace}</span>
                    <Button 
                        data-testid="notification-button"
                        className={styles.notification_button}
                        text 
                        style={{marginRight: 50, background: "transparent", border: "none", boxShadow: "none", outline: "none"}}>
                            <i data-testid="badge" className="pi pi-bell p-overlay-badge" style={{ fontSize: 21}}></i>
                    </Button>
                </div>
                <div className={styles.line}/>
            </div>
        </div>
    )
}

export default Header;