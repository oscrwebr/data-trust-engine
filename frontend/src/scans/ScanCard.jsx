import "./scans.css";
import { PiFileMagnifyingGlass, PiFolders } from "react-icons/pi";
import { PiCheckCircle } from "react-icons/pi";
import { PiClockClockwise } from "react-icons/pi";
import { Divider } from 'primereact/divider';



function ScanCard({ scan }) {


    // Format date into dd/mm/yyyy, hh:mm:ss
        const formatDateTime = (dateTimeString) => {
        const date = new Date(dateTimeString);
        const formattedDate = date.toLocaleDateString();
        const formattedTime = date.toLocaleTimeString();
        return `${formattedDate}, ${formattedTime}`;
    }

    // Setting the ScanCard visuals for each scan type
    // Only organisation and sensitivity type scans for now, can be adjusted to include other types if needed
    const scanTypeClassName = scan.scan_type === "organisation" 
                            ? "scan-type-organisation"
                            : "scan-type-sensitivity";

    const scanTypeIcon = scan.scan_type === "organisation"
                            ? <PiFolders/>
                            : <PiFileMagnifyingGlass/>

    const scanTypeText = scan.scan_type === "organisation"
                            ? "Organisational"
                            : "Sensitivity"

    const scanStatusIcon = scan.finished_at 
                            ? <PiCheckCircle/>
                            : <PiClockClockwise/>

    return(

        <div className={`scan-card ${scanTypeClassName}`}>
            <div className="scan-card-top">
                <div className="scan-card-top-left">
                    <span className={`scan-type-icon scan-type-icon-${scan.scan_type}`}>
                        {scanTypeIcon}
                    </span>

                    <span className={`scan-type-text scan-type-text-${scan.scan_type}`}>
                        {scanTypeText}
                    </span>
                </div>
                <div className="scan-card-top-right">
                    <span className={`scan-status-text ${scan.finished_at ? "scan-status-completed" : "scan-status-ongoing"}`}>
                        {scanStatusIcon}
                        {scan.finished_at ? "Completed" : "Ongoing"}
                    </span>
                </div>
            </div>
            <div className="scan-card-id-section">
                <span className="scan-card-id-heading">Scan ID</span>
                <span className="scan-card-id">{scan.scan_id}</span>
            </div>
            
            <span>{formatDateTime(scan.started_at)}</span>
            <span>{formatDateTime(scan.finished_at)}</span>
        </div>
    )
}

export default ScanCard;