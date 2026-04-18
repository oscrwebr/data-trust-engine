import { Avatar } from "primereact/avatar";
import { Checkbox } from 'primereact/checkbox';
import styles from "./view_employees.module.css";
import MoreInformationPanel from "./MoreInformationPanel";
import { useRef } from "react";

function SquareCard({id, initials, firstname, surname, email, role, risk, checked, onChange}){

    const op = useRef(null);

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
                <div>
                    <strong onClick={(e) => op.current.toggle(e)} className={
                        risk.id === 1 
                            ? styles.no_files_no_scan
                            : risk.id === 2
                            ? styles.no_files_no_scan
                            : risk.id === 3
                            ? styles.high_risk
                            : risk.id === 4
                            ? styles.low_risk
                            : ""
                        }>{risk.status}
                    </strong>
                    <MoreInformationPanel forwardRef={op} risk={risk}/>
                </div>
            </div>
        </div>
    )
}

export default SquareCard;