import styles from "./EmployeeAccessItem.module.css";

import { FaCheckCircle } from "react-icons/fa";
import { FaExclamationCircle } from "react-icons/fa";

function EmployeeAccessItem({ employee }) {
    return (
        <div className={styles.employee_access_item}>
            <div className={styles.employee_top_row}>
                <div className={styles.employee_name}>{employee.name}</div>
                <div className={styles.employee_email}>{employee.email}</div>
            </div>

            <div className={styles.employee_access_status_icon}>
                {employee.access_allowed ? (<FaCheckCircle className={styles.allowed_icon}/>) : (<FaExclamationCircle className={styles.denied_icon}/>)}
            </div>

            <div className={styles.employee_roles}>
                <div className={styles.roles_label}>Roles:</div>{" "}
                {employee.roles.length > 0 ? employee.roles.join(", ") : "No roles assigned"}
            </div>
        </div>
    );
}


export default EmployeeAccessItem;