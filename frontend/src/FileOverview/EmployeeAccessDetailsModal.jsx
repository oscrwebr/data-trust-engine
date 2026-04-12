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

                    <button className={styles.close_icon_button} onClick={onClose} data-testid="close-modal-button">
                        <FaTimes />
                    </button>
                </div>

                <div className={styles.modal_warning_box}>
                    This file contains <strong>sensitive data</strong> that exceeds this employee's role thresholds:
                </div>

                <div className={styles.table_wrapper}>
                    <div className={styles.table_header}>
                        <div>Data Type</div>
                        <div>Occurrences</div>
                        <div>Threshold</div>
                    </div>

                    {employee.failed_detections.map((detection, index) => {
                        const formatted_subcategory =
                            detection.subcategory === "NO_ROLES_ASSIGNED"
                                ? "No roles assigned"
                                : detection.subcategory;

                        return (
                            <div key={index} className={styles.table_row}>
                                <div>{formatted_subcategory}</div>
                                <div>{detection.count ?? "-"}</div>
                                <div>
                                    {detection.threshold === null || detection.threshold === undefined || detection.threshold === 0
                                        ? "Not permitted"
                                        : `Maximum ${detection.threshold}`}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    )
}


export default EmployeeAccessDetailsModal;