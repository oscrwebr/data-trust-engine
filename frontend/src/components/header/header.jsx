import {useState, useEffect, useRef} from "react"
import styles from "./header.module.css"
import { FiSidebar } from "react-icons/fi";
import Notification from "../notifications/Notification.jsx";
import { Button } from "primereact/button";
import { Badge } from "primereact/badge"

function Header({firstname, lastname, workspace, sidebarVisible, setSidebarVisible, toastRef, notifications = []}){
    const [isNotificationsVisible, setIsNotificationsVisible] = useState(false);
    const notificationCount = notifications.length;

    let displayValue = '';

    if (notificationCount === 0) {
        displayValue = ''; 
    } else if (notificationCount > 5) {
        displayValue = '5+'; 
    } else {
        displayValue = notificationCount;
    }
    
    function handleNotifications(){
        setIsNotificationsVisible((prev) => !prev);
        if (!isNotificationsVisible) {
        notifications.forEach(notification => {
        toastRef.current.show({
            id: notification.id,
            severity: 'info', 
            sticky: true, 
            closable: true,
            content: (props) => (
            <Notification 
                key={notification.id}
                title={notification.title}
                body={notification.body}
                date={notification.datetime}
            />
            ),
        });
        });
        } else {
            toastRef.current.clear();
        }
    }
    console.log("Notifications", notifications)
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
                        onClick={handleNotifications}
                        text 
                        style={{marginRight: 30, background: "transparent", border: "none", boxShadow: "none", outline: "none"}}>
                            <i data-testid="badge" className="pi pi-bell p-overlay-badge" style={{ fontSize: 21}}>{notificationCount > 0 && <Badge value={displayValue} severity="danger" />}</i>
                    </Button>
                </div>
                <div className={styles.line}/>
            </div>
        </div>
    )
}

export default Header;