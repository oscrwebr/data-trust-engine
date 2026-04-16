import { use, useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import "../scans/scans.css";


function ScanFile({ scan_file }) {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [scanFile, setScanFile] = useState(null);
    const scanFileId = useParams()

//     useEffect(() => {
//         api.get(`/scanning/`)

// }, [scanFileId])

    return (
        <div>
            {loading ? (
                    <p className="scan-loading">Loading scanned file...</p>
                ) : error ? (
                    <p className="scan-loading">Error loading scanned file.</p>
                ) : scanFile === null ? (
                    <p className="scan-loading">No scanned file found.</p>
                ) : ScanTypePage ? ( 
                    <>
                        <div className="scan-header">
                            <h1 className="scan-heading">
                                Scan File {scan_file.scan_file_id} Results
                            </h1>
                        </div>
                    </>
                ) : (
                    <p className="scan-loading">Error fetching scan file.</p>
                )}
        </div>
        
    )
}

export default ScanFile;