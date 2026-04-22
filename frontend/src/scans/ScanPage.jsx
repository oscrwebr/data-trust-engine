import { useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import './scans.css';
import api from "../api/axiosConfig";
import { Link, useParams } from "react-router-dom";
import OrganisationScanPage from "./OrganisationScanPage";
import SensitivityScanPage from "./SensitivityScanPage";

import { formatDateTime } from "./utils/formatDateTime";

function ScanPage() {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [scan, setScan] = useState(null);
    const {scanId} = useParams();
    // Used to determine what type of ScanPage to load rather than having multiple if statements 
    // Better for scalability and ability to plug new scan types in
    const scanPageTypes = {
        organisation: OrganisationScanPage,
        sensitivity: SensitivityScanPage
    }

    // Get scan details through ID
    useEffect(() => {
        api.get(`/scanning/get_scan_by_id/${scanId}`)
        .then(response => {
            setLoading(false);
            setScan(response.data);
        })
        .catch(error => {
            console.error("Error fetching scan:", error);
            setError(error);
            setLoading(false);
        })
    }, [scanId])

    // Fetches the page type to render
    const ScanTypePage = scan ? scanPageTypes[scan.scan_type] : null;

    return (
        <div>
            <div>
                {loading ? (
                    <p className="scan-loading">Loading scan...</p>
                ) : error ? (
                    <p className="scan-loading">Error loading scan.</p>
                ) : scan === null ? (
                    <p className="scan-loading">No scan found.</p>
                ) : ScanTypePage ? (
                    <>
                        {/* Heading portion */}
                        <div className="scan-header">
                            <h1 className="scan-heading">
                                Scan {scan.scan_id} Results
                            </h1>
                            <p className="scan-loading">
                                Type: {scan.scan_type.charAt(0).toUpperCase() + scan.scan_type.slice(1)} | Finished At: {formatDateTime(scan.finished_at)}
                            </p>
                        <Divider/>
                        </div>

                        {/* Render the type of page depending on scan type (only organisation and sensitivity as of now) */}
                        <ScanTypePage scan={scan} />
                    </>
                ) : (
                    <p className="scan-loading">Error fetching scan type.</p>
                )}
            </div>
        </div>



    )
}

export default ScanPage;