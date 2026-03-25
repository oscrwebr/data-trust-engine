import { Avatar } from "primereact/Avatar";
import styles from "./employees.module.css"
import { Button } from "primereact/button";

function RowCard({initials, firstname, surname, email, role}){
    return(
        <div className={styles.row_card_container}>
            <Avatar className={styles.row_avatar} label={initials} shape="circle" />
            <div className={styles.row_info}>
                <span className={styles.row_name}>{firstname} {surname}</span>
                <span className={styles.row_email}>{email}</span>
                <span className={styles.row_role}>{role}</span>
                <strong className={styles.row_risk}>Scanning Risk</strong>
            </div>
            <Button className={styles.row_send_button}>Send Message</Button>
        </div>
    )
}

export default RowCard;