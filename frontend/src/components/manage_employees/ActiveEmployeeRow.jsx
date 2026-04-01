import styles from "./manage_employees.module.css"

import { Avatar } from "primereact/Avatar";
import { Dropdown } from "primereact/dropdown";
import { Button } from "primereact/button";

function ActiveEmployeeRow({initials, firstname, surname, email, employeeRole, roles, setEmployeeRole}){
    
    return(
        <div className={styles.row_card_container}>
            <Avatar className={styles.row_avatar} label={initials} shape="circle" />
            <div className={styles.row_info}>
                <span className={styles.row_name}>{firstname} {surname}</span>
                <span className={styles.row_email}>{email}</span>
                <Dropdown value={employeeRole} className="p-inputtext-sm" optionLabel="name" optionValue="name" options={roles} onChange={(e) => setEmployeeRole(e.value)}/>
                <Button className={styles.remove_button} label="Remove" severity="danger"/>
            </div>
        </div>
    )
}

export default ActiveEmployeeRow;