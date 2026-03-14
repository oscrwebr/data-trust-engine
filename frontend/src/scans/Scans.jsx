import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
// import { DataTable } from 'primereact/datatable';
// import { Column } from 'primereact/column';
import { Link } from "react-router-dom";
import ScanCard from "./ScanCard";
import { Divider } from 'primereact/divider';
import "./scans.css";


function Scans(){


    const [scans, setScans] = useState([]);

    // Get scans from /get_all_scans endpoint
    useEffect(() => {
        api.get("/scanning/get_all_scans")

        .then(response => {
            setScans(response.data);
        })

        .catch(error => {
        console.error("Error fetching scans:", error);
        });

    }, []);


    return (
        <div>
            <div className="scan-header">
                <h1 className="scan-heading">Scans</h1>
                <Divider/>
            </div>
            
            <div className="scan-grid">
                {scans.map(scan => (
                    <ScanCard key={scan.scan_id} scan={scan}/>
                ))}
            </div>
        </div>
    );
}

export default Scans;