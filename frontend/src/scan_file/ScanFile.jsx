import { use, useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import "../scans/scans.css";
import api from "../api/axiosConfig";
import { Link, useParams } from "react-router-dom";
import "./scan_file.css";
import { useNavigate } from "react-router-dom";
import { PiArrowLeftBold } from "react-icons/pi";
import { getSensitivityScanPageCardClass } from "../scans/utils/getSensitivityScanPageCardClass";
import { PiScalesBold } from "react-icons/pi";
import { PiCurrencyGbpBold } from "react-icons/pi";
import { PiUserListBold } from "react-icons/pi";
import { PiFileMagnifyingGlass } from "react-icons/pi";




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
                                <PiArrowLeftBold />
                                Back
                            </button>
                        </div>
                        <Divider/>
                        <div className="sensitivity-scan-page-file-container">
                            <div className="scan-page-card">
                                <div className="scan-page-card-text">
                                    <span className="scan-page-card-subtitle">Total Detections</span>
                                    <span className="scan-page-card-title">{scanFile?.category_counts ? scanFile.category_counts.personal + scanFile.category_counts.legal_case + scanFile.category_counts.financial : 0}</span>
                                    
                                </div>
                                <div className="scan-page-card-image">
                                    <PiFileMagnifyingGlass size={30}/>
                                </div>
                            </div>
                            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scanFile.category_counts.personal, 1)}`}>
                                <div className="scan-page-card-text">
                                    <span className="scan-page-card-subtitle">PII Detections</span>
                                    <span className="scan-page-card-title">{scanFile.category_counts.personal}</span>
                                    
                                </div>
                                <div className="scan-page-card-image">
                                    <PiUserListBold size={30}/>
                                </div>
                            </div>
                            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scanFile.category_counts.legal_case, 1)}`}>
                                <div className="scan-page-card-text">
                                    <span className="scan-page-card-subtitle">Legal Detections</span>
                                    <span className="scan-page-card-title">{scanFile.category_counts.legal_case}</span>
                                    
                                </div>
                                <div className="scan-page-card-image">
                                    <PiScalesBold size={30}/>
                                </div>
                            </div>
                            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scanFile.category_counts.financial, 1)}`}>
                                <div className="scan-page-card-text">
                                    <span className="scan-page-card-subtitle">Financial Detections</span>
                                    <span className="scan-page-card-title">{scanFile.category_counts.financial}</span>
                                    
                                </div>
                                <div className="scan-page-card-image">
                                        <PiCurrencyGbpBold size={30}/>
                                    
                                </div>
                            </div>
                        </div>
                        
                    </>
                )}
        </div>
        
    )
}

export default ScanFile;