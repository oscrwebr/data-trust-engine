import { Avatar } from "primereact/Avatar";
import { Checkbox } from 'primereact/checkbox';
import styles from "./employees.module.css"

function RowCard({id, initials, firstname, surname, email, role, checked, onChange}){
    return(
        <div className={styles.row_card_container}>
            <Avatar className={styles.row_avatar} label={initials} shape="circle" />
            <div className={styles.row_info}>
                <span className={styles.row_name}>{firstname} {surname}</span>
                <span className={styles.row_email}>{email}</span>
                <span className={styles.row_role}>{role}</span>
                <strong className={styles.row_risk}>Scanning Risk</strong>
            </div>
            <div className="card flex justify-content-center" style={{ margin: " 0 29px" }}>
                <Checkbox inputId={id} onChange={(e) => onChange(id, e.checked)} checked={checked} />
            </div>
        </div>
    )
}

export default RowCard;