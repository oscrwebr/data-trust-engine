import { Avatar } from "primereact/Avatar";
import { Checkbox } from 'primereact/checkbox';
import styles from "./view_employees.module.css"

function SquareCard({id, initials, firstname, surname, email, role, checked, onChange}){
    return(
        <div className={styles.square_card_container} data-testid={`square-${id}`}>
            <div className={styles.checkbox_container} style={{ marginRight: "8px" }}>
                <Checkbox data-testid="square-checkbox" inputId={id} onChange={(e) => onChange(id, e.checked)} checked={checked} />
            </div>
            <Avatar className={styles.square_avatar} label={initials} shape="circle" />
            <div className={styles.square_info}>
                <span className={styles.square_name}>{firstname} {surname}</span>
                <span className={styles.square_email}>{email}</span>
                <span className={styles.square_role}>{role}</span>
                <strong className={styles.square_risk}>Scanning Risk</strong>
            </div>
        </div>
    )
}

export default SquareCard;