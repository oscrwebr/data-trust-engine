import { useState } from "react";
import styles from "./EmployeeAccessItem.module.css";
import EmployeeAccessDetailsModal from "./EmployeeAccessDetailsModal";

import { FaCheckCircle } from "react-icons/fa";
import { FaExclamationCircle } from "react-icons/fa";

function EmployeeAccessItem({ employee }) {
    const [show_modal, set_show_modal] = useState(false);

    return (
        <>
            <div className={styles.employee_access_item}>
                <div className={styles.employee_access_status_icon}>
                    {employee.access_allowed ? (
                        <FaCheckCircle 
                            className={styles.allowed_icon}
                            data-testid="allowed-icon"
                        />
                    ) : (
                        <FaExclamationCircle 
                            className={styles.denied_icon}
                            data-testid="denied-icon"
                        />
                    )}
                </div>

                <div className={styles.employee_content}>
                    <div className={styles.employee_information}>
                        <div className={styles.employee_name}>{employee.name}</div>
                        <div className={styles.employee_email}>{employee.email}</div>
                    </div>

                    <div className={styles.employee_roles}>
                        <div>
                            {employee.roles.length > 0 ? employee.roles.join(", ") : "No roles assigned"}
                        </div>
                    </div>

                    {!employee.access_allowed && (
                        <button className={styles.more_details_button} onClick={() => set_show_modal(true)}>More Details</button>
                    )}
                </div>
            </div>

            {show_modal && (
                <EmployeeAccessDetailsModal employee={employee} onClose={() => set_show_modal(false)}/>
            )}
        </>
    );
}


export default EmployeeAccessItem;