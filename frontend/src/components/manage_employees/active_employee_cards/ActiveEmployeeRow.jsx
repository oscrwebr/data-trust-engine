import styles from "../manage_employees.module.css"
import api from "../../../api/axiosConfig"
import { Avatar } from "primereact/Avatar";
import { Dropdown } from "primereact/dropdown";
import { Button } from "primereact/button";

function ActiveEmployeeRow({id, initials, firstname, surname, email, employeeRole, roles, setEmployeeRole, removeEmployee}){
    return(
        <div className={styles.row_card_container} data-testid={`row-${id}`}>
            <Avatar className={styles.row_avatar} label={initials} shape="circle" />
            <div className={styles.row_info}>
                <span className={styles.row_name}>{firstname} {surname}</span>
                <span className={styles.row_email}>{email}</span>
                <Dropdown data-testid="row-role-dropdown" value={employeeRole} className="p-inputtext-sm" optionLabel="name" optionValue="name" options={roles} onChange={(e) => setEmployeeRole(e.value)}/>
                <Button data-testid={`remove-button-${id}`} onClick={removeEmployee} className={styles.remove_button} label="Remove" severity="danger"/>
            </div>
        </div>
    )
}

export default ActiveEmployeeRow;