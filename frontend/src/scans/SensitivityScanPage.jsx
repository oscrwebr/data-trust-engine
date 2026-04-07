import { PiCurrencyGbpBold } from "react-icons/pi";
import { PiScalesBold } from "react-icons/pi";
import { PiUserListBold } from "react-icons/pi";
import { PiFileBold } from "react-icons/pi";
import { PiCheckCircleBold } from "react-icons/pi";
import { PiWarningCircleBold } from "react-icons/pi";
import ScanFileCard from "./ScanFileCard";
import { getScanPageCardClass } from "./utils/getScanPageCardClass";
import { getPercentage } from "./utils/getPercentage";
import { getCleanFilesClass } from "./utils/getCleanFilesClass";
import { formatNamingConventionName } from "./utils/formatNamingConventionName";
import { getSensitivityScanPageCardClass } from "./utils/getSensitivityScanPageCardClass";

function SensitivityScanPage({ scan }) {

    

    return (
        <>
        {/* To change the colour of a card, apply either 'critical' 'issues' or 'clean' to the scan-page-card class */}
        <div className="sensitivity-scan-page-file-container">
            <div className="scan-page-card">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Total Files Scanned</span>
                    <span className="scan-page-card-title">{scan.file_count}</span>
                    
                </div>
                <div>
                    <PiFileBold size={50}/>
                </div>
            </div>
            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scan.detection_counts.personal, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">PII Detections</span>
                    <span className="scan-page-card-title">{scan.detection_counts.personal}</span>
                    
                </div>
                <div>
                    <PiUserListBold size={50}/>
                </div>
            </div>
            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scan.detection_counts.financial, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Financial Detections</span>
                    <span className="scan-page-card-title">{scan.detection_counts.financial}</span>
                    
                </div>
                <div>
                    <PiCurrencyGbpBold size={50}/>
                </div>
            </div>

            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scan.detection_counts.legal_case, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Legal Detections</span>
                    <span className="scan-page-card-title">{scan.detection_counts.legal_case}</span>
                    
                </div>
                <div>
                    <PiScalesBold size={50}/>
                </div>
            </div>
            <div className={"scan-page-card critical"}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">High Risk Files</span>
                    {/* HARDCODED FOR NOW... */}
                    <span className="scan-page-card-title">1</span>
                    
                </div>
                <div>
                    <PiWarningCircleBold size={50}/>
                </div>
            </div>
            
        </div>
        <h2 className="scan-page-files-heading">All Scanned Files</h2>

        <div className="scan-page-file-container">
            {scan.files.map(scan_file => (
                <ScanFileCard key={scan_file.scan_file_id} scan_file={scan_file} scan_type={scan.scan_type}/>
            ))}
        </div>
        </>
        

    )
}

export default SensitivityScanPage;