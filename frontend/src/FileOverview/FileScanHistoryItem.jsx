function FileScanHistoryItem({ scan }) {
    return (
        <div className="history-item">
            <p>{new Date(scan.started_at).toLocaleString()}</p>
            <div>{scan.finished_at ? "Completed" : "In Progress"}</div>
        </div>
    )
}


export default FileScanHistoryItem;