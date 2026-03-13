import { use, useEffect, useState } from "react";
import axios from "axios";

function Scans(){


    const [scans, setScans] = useState([]);

    // Get scans from /get_scans endpoint
    useEffect(() => {
        axios.get("/api/scanning/get_scans")

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
                        <li key={scan.id}>{scan.name}</li>
                    ))}
                </ul>
        </div>
    );
}

export default Scans;