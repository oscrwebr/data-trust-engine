function ScanFileCard({scan_file}) {
    return (
        <div key={scan_file.file_id} className="scan-page-file-card">
            <p>{scan_file.file_name}</p>
        </div>
    )
}

export default ScanFileCard;