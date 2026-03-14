import "./scans.css";

function ScanCard({ scan }) {

        const formatDateTime = (dateTimeString) => {
        const date = new Date(dateTimeString);
        const formattedDate = date.toLocaleDateString();
        const formattedTime = date.toLocaleTimeString();
        return `${formattedDate}, ${formattedTime}`;
    }

    return(

        <div className="scan-card">
            <span>{scan.scan_id}</span>
        </div>
    )
}

export default ScanCard;