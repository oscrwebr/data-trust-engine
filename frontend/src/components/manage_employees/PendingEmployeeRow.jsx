import styles from "./manage_employees.module.css"

import { Avatar } from "primereact/Avatar";
import { Button } from "primereact/button";

function PendingEmployeeRow({email, status}){
    return(
        <div className={styles.row_card_container}>
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
        </div>
    )
}

export default PendingEmployeeRow;