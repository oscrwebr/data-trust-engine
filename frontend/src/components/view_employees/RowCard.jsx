import { Avatar } from "primereact/avatar";
import { Checkbox } from 'primereact/checkbox';
import styles from "./view_employees.module.css"
import MoreInformationPanel from "./MoreInformationPanel";
import { useRef } from "react";

function RowCard({id, initials, firstname, surname, email, role, risk, checked, onChange}){

    const op = useRef(null);

    return(
        <div className={styles.row_card_container} data-testid={`row-${id}`}>
            <Avatar className={styles.row_avatar} label={initials} shape="circle" />
            <div className={styles.row_info}>
                <span className={styles.row_name}>{firstname} {surname}</span>
                <span className={styles.row_email}>{email}</span>
                <span className={styles.row_role}>{role}</span>
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
            <div className="card flex justify-content-center" style={{ margin: " 0 29px" }}>
                <Checkbox data-testid={`checkbox-${id}`} inputId={id} onChange={(e) => onChange(id, e.checked)} checked={checked} />
            </div>
        </div>
    )
}

export default RowCard;