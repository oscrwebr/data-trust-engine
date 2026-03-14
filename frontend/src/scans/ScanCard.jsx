import "./scans.css";
import { PiFileMagnifyingGlass, PiFolders } from "react-icons/pi";
import { PiCheckCircle } from "react-icons/pi";
import { PiClockClockwise } from "react-icons/pi";
import { Divider } from 'primereact/divider';
import { PiWarningCircle } from "react-icons/pi";




function ScanCard({ scan }) {


    // Format date into dd/mm/yyyy, hh:mm:ss
        const formatDateTime = (dateTimeString) => {
            // For ongoing scans... Display "-" as the Finished At time
            if (!dateTimeString) {
                return "-";
            }
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
            {/* Top section of the ScanCard split into two sections */}
            <div className="scan-card-top">
                {/* Top left displays type of scan */}
                <div className="scan-card-top-left">
                    {/* Scan type icon */}
                    <span className={`scan-type-icon scan-type-icon-${scan.scan_type}`}>
                        {scanTypeIcon}
                    </span>
                    {/* Scan type text */}
                    <span className={`scan-type-text scan-type-text-${scan.scan_type}`}>
                        {scanTypeText}
                    </span>
                </div>
                {/* Top right displays the scan status */}
                <div className="scan-card-top-right">
                    {/* Scan status can be either completed or ongoing (could modify to include failed in future) */}
                    <span className={`scan-status-text ${scan.finished_at ? "scan-status-completed" : "scan-status-ongoing"}`}>
                        {scanStatusIcon}
                        {scan.finished_at ? "Completed" : "Ongoing"}
                    </span>
                </div>
            </div>
            {/* Scan ID section */}
            <div className="scan-card-id-section">
                <span className="scan-card-id-heading">Scan ID</span>
                <span className="scan-card-id">{scan.scan_id}</span>
            </div>
            {/* Scan Started At and Finished At section */}
            <div className="scan-card-dates">
                {/* Started At block */}
                <div className="scan-card-date-block">
                    <span className="scan-card-id-heading">Started At</span>
                    <span className="scan-card-value">
                        {formatDateTime(scan.started_at)}
                    </span>
                </div>
                {/* Finished At block */}
                <div className="scan-card-date-block">
                    <span className="scan-card-id-heading">Finished At</span>
                    <span className="scan-card-value">
                        {formatDateTime(scan.finished_at)}
                    </span>
                </div>
            </div>
            {/* From PrimeReact: https://primereact.org/divider/ */}
            <Divider/>
            <div className="scan-card-dates">
                <div className="scan-card-date-block">
                    <span className="scan-card-id-heading">Total Files</span>
                    <span className="scan-card-value scan-card-total-files">
                        5
                    </span>
                </div>
                <div className="scan-card-date-block">
                    <span className="scan-card-id-heading">Files with Issues</span>
                    <span className="scan-card-value scan-card-issue-files">
                        2
                    </span>
                </div>
            </div>
        </div>
    )
}

export default ScanCard;