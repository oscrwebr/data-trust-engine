import { useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import './scans.css';
import api from "../api/axiosConfig";
import { Link, useParams } from "react-router-dom";
import OrganisationScanPage from "./OrganisationScanPage";
import SensitivityScanPage from "./SensitivityScanPage";

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

    const ScanTypePage = scan ? scanPageTypes[scan.scan_type] : null;

    return (
        <div>
            <div className="scan-header">
                <h1 className="scan-heading">
                    {scan ? `Scan ${scan.scan_id}` : 'Unknown Scan'}
                </h1>
                <Divider/>
            </div>

            <div>
                {loading ? (
                    <p className="scan-loading">Loading scan...</p>
                ) : error ? (
                    <p className="scan-loading">Error loading scan.</p>
                ) : scan === null ? (
                    <p className="scan-loading">No scan found.</p>
                ) : ScanTypePage ? (
                    // Render the type of page depending on scan type (only organisation and sensitivity as of now)
                    <ScanTypePage scan={scan} />
                ) : (
                    <p className="scan-loading">Error fetching scan type.</p>
                )}
            </div>
        </div>



    )
}

export default ScanPage;