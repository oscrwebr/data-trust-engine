import styles from "../manage_employees.module.css"
import { Avatar } from "primereact/Avatar";
import { Button } from "primereact/button";
import dayjs from "dayjs";

function PendingEmployeeSquare({email, status, datetime, onReject, onAccept}){

    const d = dayjs(datetime);
    
    const date = d.format("D MMMM YYYY");
    const time = d.format("HH:mm:ss");

    return(
        <div className={styles.square_card_container_pending}>
            
            {status === "request" && (
                <>
                    <div className={styles.icon_container}>
                        <i id={styles.request_icon} className="pi pi-user-plus"/>
                    </div>
                    <Avatar className={styles.square_avatar} label="" shape="circle" />
                    <div className={styles.square_info}>
                        <span className={styles.square_email}>{email}</span>
                        <div className={styles.square_button_container}>
                            <Button onClick={onAccept} className={styles.square_accept_button}>Accept</Button>
                            <Button onClick={onReject} className={styles.square_reject_button}>Reject</Button>
                        </div>
                    </div>
                </>
            )}

            {status === "invite" && (
                <>  
                    <div className={styles.icon_container}>
                        <i id={styles.invite_icon} className="pi pi-clock"/>
                    </div>
                    <Avatar className={styles.square_avatar} label="" shape="circle" />
                    <div className={styles.square_info}>
                        <span className={styles.square_email}>{email}</span>
                        <span className={styles.invite_sent_text}>Invite sent on the <br/>{date} at {time}</span>
                    </div>
                </>
            )}
        </div>
    )
}

export default PendingEmployeeSquare;