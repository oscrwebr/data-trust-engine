import styles from "./manage_employees.module.css"

import { Avatar } from "primereact/Avatar";
import { Dropdown } from "primereact/dropdown";

function ActiveEmployeeSquare({initials, firstname, surname, email, employeeRole, roles, setEmployeeRole, onRemove}){
    return(
        <div className={styles.square_card_container}>
            <div className={styles.icon_container}>
                <i onClick={onRemove} id={styles.remove_icon} className="pi pi-times"/>
            </div>
            <Avatar className={styles.square_avatar} label={initials} shape="circle" />
            <div className={styles.square_info}>
                <span className={styles.square_name}>{firstname} {surname}</span>
                <span className={styles.square_email}>{email}</span>
                <Dropdown value={employeeRole} className="p-inputtext-sm" optionLabel="name" optionValue="name" options={roles} onChange={(e) => setEmployeeRole(e.value)}/>
            </div>
        </div>
    )
}

export default ActiveEmployeeSquare;