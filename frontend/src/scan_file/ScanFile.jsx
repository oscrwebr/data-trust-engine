import { use, useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import "../scans/scans.css";
import api from "../api/axiosConfig";
import { Link, useParams } from "react-router-dom";
import "./scan_file.css";
import { useNavigate } from "react-router-dom";


function ScanFile({ scan_file }) {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [scanFile, setScanFile] = useState(null);
    const { scanFileId } = useParams();

    const navigate = useNavigate();

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
                        <div className="scan-file-header">
                            <div className="scan-file-header-left">
                                <h1 className="scan-heading">
                                    {scanFile.file_name}
                                </h1>
                                <p className="scan-loading">
                                    Scan ID: {scanFile.scan_id} | Scan File ID: {scanFile.scan_file_id}
                                </p>
                            </div>
                            <button className="back-button" onClick={() => navigate(`/scans/${scanFile.scan_id}`)}>
                                Back
                            </button>
                        </div>
                    </>
                )}
        </div>
        
    )
}

export default ScanFile;