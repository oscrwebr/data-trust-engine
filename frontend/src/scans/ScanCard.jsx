import "./scans.css";
import { PiFileMagnifyingGlass, PiFolders } from "react-icons/pi";


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

    return(

        <div className={`scan-card ${scanTypeClassName}`}>
            <span>{scan.scan_id}</span>
            <span>{formatDateTime(scan.started_at)}</span>
            <span>{formatDateTime(scan.finished_at)}</span>
        </div>
    )
}

export default ScanCard;