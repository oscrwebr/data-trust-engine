import styles from "./FileOverview.module.css";
import { FaRegCalendarAlt } from "react-icons/fa";


function FileScanHistoryItem({ scan }) {
    const formatted_finish_date = new Date(scan.finished_at).toLocaleString("en-GB", {
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    });
    const is_completed = !!scan.finished_at;

    return (
        <div className={styles.file_scan_history_item}>
            <div className={styles.item_left_section}>
                <div className={styles.item_date_wrapper}>
                    <FaRegCalendarAlt className={styles.item_date_icon} />
                    <div className={styles.item_date}>{formatted_finish_date}</div>
                </div>
            </div>

            <div className={styles.item_right_section}>
                <div className={styles.item_detection_count}>
                    {scan.detection_count}{" "}
                    {scan.detection_count === 1 ? "detection" : "detections"}
                </div>

                <div className={`${styles.item_status} ${is_completed ? styles.completed : styles.in_progress}`}>
                    {is_completed ? "Completed" : "In Progress"}</div>
            </div>
        </div>
    )
}


export default FileScanHistoryItem;