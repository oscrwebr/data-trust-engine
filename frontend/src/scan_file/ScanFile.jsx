import { use, useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import "../scans/scans.css";
import api from "../api/axiosConfig";
import { Link, useParams } from "react-router-dom";
import "./scan_file.css";
import { useNavigate } from "react-router-dom";
import { PiArrowLeftBold, PiFile } from "react-icons/pi";
import { getSensitivityScanPageCardClass } from "../scans/utils/getSensitivityScanPageCardClass";
import { PiScalesBold } from "react-icons/pi";
import { PiCurrencyGbpBold } from "react-icons/pi";
import { PiUserListBold } from "react-icons/pi";
import { PiFileMagnifyingGlass } from "react-icons/pi";
import { Accordion, AccordionTab } from 'primereact/accordion';
import { PiFileText } from "react-icons/pi";
import { PiMagnifyingGlassBold } from "react-icons/pi";
import { PiFileBold } from "react-icons/pi";
import { PiHash } from "react-icons/pi";






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

    // Group detections by page number
    const pageDetections = {}

    // Loop through each detection and add to the dictionary
    // ?? [] used for Organisational scan_files which don't use detections (stops crash)
    for (const detection of scanFile?.detections ?? []) {
        const page = detection.page_number;
        if (!pageDetections[page]) {
            pageDetections[page] = [];
        }
        pageDetections[page].push(detection);
    }

    // Get the counts for each page
    const pageDetectionCounts = {}

    for (const page in pageDetections) {
        pageDetectionCounts[page] = pageDetections[page].length;
    }

    // Sort the pages so they are in the correct order (Page 1 FIRST, Page 2 etc.)
    const sortedPages = Object.keys(pageDetections).map(Number).sort((a, b) => a - b);

    // Rendering icons depending on value returned
    // Adapted from: https://stackoverflow.com/a/53727367
    const categoryIcons = {
        "PERSONAL": <PiUserListBold size={20} />,
        "LEGAL CASE": <PiScalesBold size={20} />,
        "FINANCIAL": <PiCurrencyGbpBold size={20}/>
    }

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
                                <div className="pills">
                                    <button className="header-pill" onClick={() => navigate(`/scan-file/${scanFile.scan_file_id}`)}>
                                        <PiHash />
                                        Scan File ID: {scanFile.scan_file_id}
                                    </button>
                                    <button className="header-pill" onClick={() => navigate(`/scans/${scanFile.scan_id}`)}>
                                        <PiMagnifyingGlassBold />
                                        Scan ID: {scanFile.scan_id}
                                    </button>
                                    <button className="header-pill" onClick={() => navigate(`/files/${scanFile.file_id}`)}>
                                        <PiFileBold />
                                        File ID: {scanFile.file_id}
                                    </button>
                                </div>
                            </div>
                            <button className="back-button" onClick={() => navigate(-1)}>
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
                                    <div className="icon-box">
                                    <PiFileMagnifyingGlass size={30}/>
                                    </div>
                                </div>
                            </div>
                            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scanFile.category_counts.personal, 1)}`}>
                                <div className="scan-page-card-text">
                                    <span className="scan-page-card-subtitle">PII</span>
                                    <span className="scan-page-card-title">{scanFile.category_counts.personal}</span>
                                    
                                </div>
                                <div className="scan-page-card-image">
                                    <div className="icon-box">
                                    <PiUserListBold size={30}/>
                                    </div>
                                </div>
                            </div>
                            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scanFile.category_counts.financial, 1)}`}>
                                <div className="scan-page-card-text">
                                    <span className="scan-page-card-subtitle">Financial</span>
                                    <span className="scan-page-card-title">{scanFile.category_counts.financial}</span>
                                    
                                </div>
                                <div className="scan-page-card-image">
                                    <div className="icon-box">
                                        <PiCurrencyGbpBold size={30}/>
                                    </div>
                                </div>
                            </div>
                            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scanFile.category_counts.legal_case, 1)}`}>
                                <div className="scan-page-card-text">
                                    <span className="scan-page-card-subtitle">Legal</span>
                                    <span className="scan-page-card-title">{scanFile.category_counts.legal_case}</span>
                                    
                                </div>
                                <div className="scan-page-card-image">
                                    <div className="icon-box">
                                    <PiScalesBold size={30}/>
                                    </div>
                                </div>
                            </div>

                            
                        </div>

                        <h2 className="scan-page-files-heading">Detections by Page</h2>

                        <div>
                            <Accordion multiple>
                                {sortedPages.map(page => (
                                    <AccordionTab key={page} header={
                                        <div className="accordion-header">
                                            <div className="accordion-icon">
                                                <PiFileText size={35}/>
                                            </div>
                                            <div className="accordion-header-text">
                                                <div className="accordion-heading">
                                                    <span>{`Page ${page}`}</span>
                                                </div>
                                                <div className="accordion-heading-detections">
                                                    <span>{pageDetectionCounts[page]} {pageDetectionCounts[page] === 1 ? 'Detection' : 'Detections'}</span>
                                                </div>
                                            </div>
                                        </div>
                                    }>   

                                        <div className="detection-rows">
                                        {pageDetections[page].map((detection, index) => (
                                            <div key={detection.scan_file_detection_id} className="detection-row">
                                                <span className="pill">
                                                    {categoryIcons[detection.category.toUpperCase()]}
                                                    {detection.category}
                                                </span>
                                                <span className="detection-text">{detection.subcategory}</span>
                                                <span>Line {index+1}</span>
                                            </div>
                                        ))}
                                        </div>
                                    </AccordionTab>
                                ))}
                            </Accordion>
                        </div>                        
                    </>
                )}
        </div>
        
    )
}

export default ScanFile;