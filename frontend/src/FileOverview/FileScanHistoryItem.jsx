function FileScanHistoryItem({ scan }) {
    return (
        <div className="history-item">
            <div>
                <div>{new Date(scan.started_at).toLocaleString()}</div>
            </div>

            <div>
                <div>{scan.detection_count} detections</div>
                <div>{scan.finished_at ? "Completed" : "In Progress"}</div>
            </div>
        </div>
    )
}


export default FileScanHistoryItem;