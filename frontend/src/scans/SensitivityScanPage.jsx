import { PiFileBold } from "react-icons/pi";
import { PiTextAaBold } from "react-icons/pi";
import { PiCardsBold } from "react-icons/pi";
import { PiCheckCircleBold } from "react-icons/pi";
import ScanFileCard from "./ScanFileCard";
import { getScanPageCardClass } from "./utils/getScanPageCardClass";
import { getPercentage } from "./utils/getPercentage";
import { getCleanFilesClass } from "./utils/getCleanFilesClass";
import { formatNamingConventionName } from "./utils/formatNamingConventionName";

function SensitivityScanPage({ scan }) {

    

    return (
        <>
        {/* To change the colour of a card, apply either 'critical' 'issues' or 'clean' to the scan-page-card class */}
        <div className="scan-page-card-container">
            <div className="scan-page-card">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Total Files Scanned</span>
                    <span className="scan-page-card-title">{scan.file_count}</span>
                    
                </div>
                <div>
                    <PiFileBold size={50}/>
                </div>
            </div>
            <div className={"scan-page-card"}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">PII Issues</span>
                    {/* HARDCODED FOR NOW */}
                    <span className="scan-page-card-title">1</span>
                    
                </div>
                <div>
                    <PiTextAaBold size={50}/>
                </div>
            </div>
            <div className="scan-page-card clean">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Financial Issues</span>
                    <span className="scan-page-card-title">1</span>
                    
                </div>
                <div>
                    <PiCardsBold size={50}/>
                </div>
            </div>

            <div className="scan-page-card clean">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Legal Issues</span>
                    <span className="scan-page-card-title">1</span>
                    
                </div>
                <div>
                    <PiCardsBold size={50}/>
                </div>
            </div>
            <div className={"scan-page-card clean"}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Clean Files</span>
                    <span className="scan-page-card-title">1%</span>
                    
                </div>
                <div>
                    <PiCheckCircleBold size={50}/>
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