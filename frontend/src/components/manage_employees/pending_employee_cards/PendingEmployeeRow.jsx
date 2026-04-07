import styles from "../manage_employees.module.css"
import dayjs from "dayjs";
import { Avatar } from "primereact/avatar";
import { Button } from "primereact/button";

function PendingEmployeeRow({email, status, datetime, onReject, onAccept}){

    const d = dayjs(datetime);

    const date = d.format("D MMMM YYYY");
    const time = d.format("HH:mm:ss");

    return(
        <div className={styles.row_card_container_pending}>
            {status === "request" && (
                <>
                    <Avatar className={styles.row_avatar} label="" shape="circle" />
                    <div className={styles.row_info}>
                        <span className={styles.row_email}>{email}</span>
                        <span className={styles.row_workspace_join_text}>This employee has requested to join your workspace</span>
                        <div>
                            <Button data-testid={`accept-button-${email}`} onClick={onAccept} className={styles.accept_button} label="Accept"/>
                            <Button data-testid={`reject-button-${email}`}  onClick={onReject} className={styles.reject_button} label="Reject"/>
                        </div>
                    </div>
                </>
            )}

            {status === "invite" && (
                <>
                    <Avatar className={styles.row_avatar} label="" shape="circle" />
                    <div className={styles.row_info}>
                        <span className={styles.row_email}>{email}</span>
                        <div className={styles.row_status_container}>
                            <span>Pending</span>
                            <i className="pi pi-clock"/>
                        </div>
                        <span className={styles.row_datetime}>An invite was sent on the {date} at {time}</span>
                    </div>
                </>
            )}
        </div>
    )
}

export default PendingEmployeeRow;