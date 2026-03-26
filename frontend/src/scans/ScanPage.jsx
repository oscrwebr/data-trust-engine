import { useEffect, useState } from "react";
import { Divider } from 'primereact/divider';
import './scans.css';
import api from "../api/axiosConfig";
import { Link, useParams } from "react-router-dom";

function ScanPage() {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [scan, setScan] = useState(null);
    const {scanId} = useParams();

    // Get scan details through ID
    useEffect(() => {
        api.get(`/scanning/get_scan_by_id/${scanId}`)
        .then(response => {
            console.log("responseeee",response.data);
            setLoading(false);
            setScan(response.data);
        })
        .catch(error => {
            console.error("Error fetching scan:", error);
            setError(error);
            setLoading(false);
        })
    }, [scanId])

    return (
        <div>
            {loading ? (
                <p className="scan-loading">Loading scan...</p>
            ) : error ? (
                <p className="scan-loading">Error loading scan.</p>
            ) : scan === null ? (
                <p className="scan-loading">No scan found.</p>
            ) : (
                <div className="scan-header">
                    <h1 className="scan-heading">Scan {scan.scan_id}</h1>
                    <Divider/>
                </div>
            )}
        </div>

    )
}

export default ScanPage;