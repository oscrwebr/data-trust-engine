import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
import ScanCard from "./ScanCard";
import { Divider } from 'primereact/divider';
import "./scans.css";
import { LuFileScan } from "react-icons/lu";


function Scans(){

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [scans, setScans] = useState([]);

    // Get scans with file count from endpoint
    useEffect(() => {
        api.get("/scanning/get_scans_with_file_count")

        .then(response => {
            setScans(response.data);
            setLoading(false);
        })

        .catch(error => {
        console.error("Error fetching scans:", error);
        setError(error);
        setLoading(false);
        });

    }, []);


    return (
        <div className="page">
            <div className="scan-header">
                <div className="header_container">
                    <LuFileScan className="header_icon"/>
                    <h1 className="title">Scans</h1>
                </div>
                
                <Divider/>
            </div>
            
            <div className="scan-grid">
                {/* Validation checks and message displays for loading/errors before finally loading the scans */}
                {loading ? (
                    <p className="scan-loading">Loading scans...</p>
                ) : error ? (
                    <p className="scan-loading">Error loading scans.</p>
                ) : scans.length === 0 ? (
                    <p className="scan-loading">No scans found.</p>
                ) : (
                    // Map scans to a ScanCard component
                    scans.map(scan => (
                        <ScanCard key={scan.scan_id} scan={scan}/>
                    ))
                )}
            </div>
        </div>
    );
}

export default Scans;