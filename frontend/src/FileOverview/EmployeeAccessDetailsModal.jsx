import styles from "./EmployeeAccessDetailsModal.module.css";
import { FaExclamationCircle, FaTimes } from "react-icons/fa";


function EmployeeAccessDetailsModal({ employee, onClose }) {
    return (
        <div className={styles.modal_overlay} onClick={onClose}>
            <div className={styles.modal_card} onClick={(event) => event.stopPropagation()}>
                <div className={styles.modal_header}>
                    <div className={styles.modal_employee_section}>
                        <div className={styles.modal_status_icon}>
                            <FaExclamationCircle className={styles.denied_icon} />
                        </div>

                        <div>
                            <div className={styles.modal_employee_name}>{employee.name}</div>
                            <div className={styles.modal_employee_email}>{employee.email}</div>
                            <div className={styles.modal_employee_roles}>{employee.roles.length > 0 ? employee.roles.join(", ") : "No roles assigned"}</div>
                        </div>
                    </div>

                    <button className={styles.close_icon_button} onClick={onClose}>
                        <FaTimes />
                    </button>
                </div>

                <div className={styles.modal_warning_box}>
                    This employee should not have access to this file.
                </div>

                <ul className={styles.failed_detection_list}>
                    {employee.failed_detections.map((detection, index) => {
                        if (detection.subcategory === "NO_ROLES_ASSIGNED") {
                            return (
                                <li key={index}>
                                    This employee has no assigned role permissions.
                                </li>
                            );
                        }

                        return (
                            <li key={index}>
                                File contains: {detection.subcategory}
                            </li>
                        );
                    })}
                </ul>

                <div className={styles.modal_footer}>
                    <button className={styles.close_button} onClick={onClose}>
                        Close
                    </button>
                </div>
            </div>
        </div>
    )
}