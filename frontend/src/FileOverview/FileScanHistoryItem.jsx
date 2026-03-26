import styles from "./FileOverview.module.css";

function FileScanHistoryItem({ scan }) {
    const formatted_finish_date = new Date(scan.finished_at).toLocaleString();
    const is_completed = !!scan.finished_at;

    return (
        <div className={styles.file_scan_history_item}>
            <div className={styles.item_left_section}>
                <div className={styles.item_date}>{formatted_finish_date}</div>
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