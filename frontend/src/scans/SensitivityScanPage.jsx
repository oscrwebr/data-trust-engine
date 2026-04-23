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
import { PiFileMagnifyingGlass } from "react-icons/pi";

function SensitivityScanPage({ scan }) {


    return (
        <>
        {/* To change the colour of a card, apply either 'critical' 'issues' or 'clean' to the scan-page-card class */}
        <div className="sensitivity-scan-page-file-container">
            <div className="scan-page-card">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Total Files</span>
                    <span className="scan-page-card-title">{scan.file_count}</span>
                    
                </div>
                <div className="scan-page-card-image">
                    <div className="icon-box">
                    <PiFileBold size={30}/>
                    </div>
                </div>
            </div>

            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scan.detection_counts.personal + scan.detection_counts.financial + scan.detection_counts.legal_case, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Total Detections</span>
                    <span className="scan-page-card-title">{scan.detection_counts.personal + scan.detection_counts.financial + scan.detection_counts.legal_case}</span>
                    
                </div>
                <div className="scan-page-card-image">
                    <div className="icon-box">
                    <PiFileMagnifyingGlass size={30}/>
                    </div>
                </div>
            </div>
            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scan.detection_counts.personal, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">PII</span>
                    <span className="scan-page-card-title">{scan.detection_counts.personal}</span>
                    
                </div>
                <div className="scan-page-card-image">
                    <div className="icon-box">
                    <PiUserListBold size={30}/>
                    </div>
                </div>
            </div>
            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scan.detection_counts.financial, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Financial</span>
                    <span className="scan-page-card-title">{scan.detection_counts.financial}</span>
                    
                </div>
                <div className="scan-page-card-image">
                    <div className="icon-box">
                    <PiCurrencyGbpBold size={30}/>
                    </div>
                </div>
            </div>

            <div className={`scan-page-card ${getSensitivityScanPageCardClass(scan.detection_counts.legal_case, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Legal</span>
                    <span className="scan-page-card-title">{scan.detection_counts.legal_case}</span>
                    
                </div>
                <div className="scan-page-card-image">
                    <div className="icon-box">
                    <PiScalesBold size={30}/>
                    </div>
                </div>
            </div>
            
            
        </div>
        <h2 className="scan-page-files-heading">All Scanned Files</h2>

        <div className="scan-page-file-container">
            {scan.files.map(scan_file => (
                <ScanFileCard key={scan_file.scan_file_id} scan_file={scan_file} scan_type={scan.scan_type} scan_files={scan.files} />
            ))}
        </div>
        </>
        

    )
}

export default SensitivityScanPage;