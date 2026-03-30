import styles from "./FileOverview.module.css";


function LatestScanResultCard({ result }) {
    return (
        <div className={styles.result_card}>
            <div className={styles.result_category}>{result.category}</div>
            <div className={styles.result_subcategory}>{result.result_subcategory}</div>
            <div className={styles.result_count}>{result.count} {result.count === 1 ? "detection" : "detections"}</div>
        </div>
    );
}


export default LatestScanResultCard;