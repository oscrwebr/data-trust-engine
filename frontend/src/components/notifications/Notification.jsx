import { Button } from "primereact/button";
import styles from "../notifications/notifications.module.css"

function Notification({title, body, date}) {
    const dateObj = new Date(date);
    const formattedDate = dateObj.toLocaleDateString('en-GB');
    const formattedTime = dateObj.toLocaleTimeString('en-GB', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false, 
    });

    return (

        // Component for holding notifications which uses PrimeReact toasts as templates
        <div className="flex flex-column align-items-left" style={{ flex: '1' }}>
            <div className={styles.n_header}>
                <strong>{title}</strong>
            </div>
            <div className={styles.n_text}>{body}</div>
            <div className={styles.n_date}>{formattedDate} at {formattedTime}</div>
        </div>
    )
}

export default Notification;