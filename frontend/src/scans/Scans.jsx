import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
// import { DataTable } from 'primereact/datatable';
// import { Column } from 'primereact/column';
import Table from '@mui/joy/Table';
import Sheet from '@mui/joy/Sheet';
import { Link } from "react-router-dom";
import ScanCard from "./ScanCard";
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
        <>
        <div className="scan-heading">
            <h1>Scans</h1>
        </div>
        <div className="scan-grid">
            {scans.map(scan => (
                <ScanCard key={scan.scan_id} scan={scan}/>
            ))}
        </div>
        </>
    );
}

export default Scans;