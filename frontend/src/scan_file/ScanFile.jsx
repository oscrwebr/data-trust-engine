import { use, useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import "../scans/scans.css";
import api from "../api/axiosConfig";
import { Link, useParams } from "react-router-dom";


function ScanFile({ scan_file }) {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [scanFile, setScanFile] = useState(null);
    const { scanFileId } = useParams();

    useEffect(() => {
        api.get(`/scanning/get_scan_file_by_id/${scanFileId}`)
        .then(response => {
            setLoading(false);
            setScanFile(response.data);
        })
        .catch(error => {
            console.error("Error fetching scanned file:", error);
            setError(error);
            setLoading(false);
        })
    }, [scanFileId])

    return (
        <div>
            {loading ? (
                    <p className="scan-loading">Loading scanned file...</p>
                ) : error ? (
                    <p className="scan-loading">Error loading scanned file.</p>
                ) : scanFile === null ? (
                    <p className="scan-loading">No scanned file found.</p>
                ) : (
                    <>
                        <div className="scan-header">
                            <h1 className="scan-heading">
                                Scan File {scanFile.scan_file_id} Results
                            </h1>
                        </div>
                    </>
                )}
        </div>
        
    )
}

export default ScanFile;