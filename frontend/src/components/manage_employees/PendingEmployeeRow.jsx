import styles from "./manage_employees.module.css"
import dayjs from "dayjs";
import { Avatar } from "primereact/Avatar";
import { Button } from "primereact/button";

function PendingEmployeeRow({email, status, datetime}){

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
                        <div className={styles.row_status_container}>
                            <span>Pending</span>
                            <i className="pi pi-clock"/>
                        </div>
                        <Button className={styles.accept_button} label="Accept"/>
                        <Button className={styles.reject_button} label="Reject"/>
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