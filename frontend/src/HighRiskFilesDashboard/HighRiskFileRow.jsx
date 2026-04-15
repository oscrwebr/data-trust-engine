import { useNavigate } from "react-router-dom";
import { FaExclamationTriangle, FaRegFileAlt } from "react-icons/fa";
import styles from "./HighRisKFileRow.module.css";

function HighRiskFileRow({ file }) {
    const navigate = useNavigate();

    function get_risk_level() {
        if (file.invalid_access_percentage >= 50) {
            return "high";
        }
        if (file.invalid_access_percentage >= 25) {
            return "medium";
        }
        return "low";
    }

    const risk_level = get_risk_level();

    return (
        <div className={styles.file_row}>
            <div className={styles.file_risk}>
                <div className={`${styles.risk_badge} ${styles[risk_level]}`}>
                    <FaExclamationTriangle />
                </div>
            </div>

            <div className={styles.file_info}>
                <div className={styles.file_icon_box}>
                    <FaRegFileAlt className={styles.file_icon}/>
                </div>
                <p className={styles.file_name}>{file.file_name}</p>
            </div>

            <div className={styles.file_access_count}>
                {file.employees_with_access_count}
            </div>

            <div className={styles.file_valid_access}>
                <div className={styles.progress_row}>
                    <div className={styles.progress_bar}>
                        <div className={styles.progress_fill} style={{ width: `${file.valid_access_percentage}%` }}/>
                    </div>

                    <p className={styles.progress_text}>
                        {Math.round(file.valid_access_percentage)}%
                    </p>
                </div>
                <div className={styles.file_access_counts}>
                    {file.valid_access_count} valid, {file.invalid_access_count} invalid
                </div>
            </div>
            
            <div className={styles.file_detections}>
                {file.detection_count} detections
            </div>

            <div className={styles.file_actions}>
                <button onClick={() => navigate(`/files/${file.file_id}`)}>
                    More Details →
                </button>
            </div>
        </div>
    )
}


export default HighRiskFileRow;