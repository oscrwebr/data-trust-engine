import { useEffect, useState } from "react";
import api from "../api/axiosConfig";

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
            <h1>Scans</h1>
                <ul>
                    {scans.map(scan => (
                        <li key={scan.scan_id}>Scan: {scan.scan_id}</li>
                    ))}
                </ul>
        </div>
    );
}

export default Scans;