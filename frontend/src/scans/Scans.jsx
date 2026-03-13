import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
// import { DataTable } from 'primereact/datatable';
// import { Column } from 'primereact/column';
import Table from '@mui/joy/Table';
import Sheet from '@mui/joy/Sheet';


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

    const formatDateTime = (dateTimeString) => {
        const date = new Date(dateTimeString);
        const formattedDate = date.toLocaleDateString();
        const formattedTime = date.toLocaleTimeString();
        return `${formattedDate} ${formattedTime}`;
    }


    return (
        <div>
            <h1>Scans</h1>
            <Sheet>
                {/* Table component from MUI Joy: https://mui.com/joy-ui/react-table/ */}
                <Table stickyFooter={false} stickyHeader stripe="even" variant="plain" aria-label="Scans table" hoverRow>
                    <thead>
                        <tr>
                            <th>Scan ID</th>
                            <th>Started At</th>
                            <th>Finished At</th>
                        </tr>
                    </thead>
                    <tbody>
                        {scans.map((scan) => (
                            <tr key={scan.scan_id}>
                                <td>{scan.scan_id}</td>
                                <td>{formatDateTime(scan.started_at)}</td>
                                <td>{formatDateTime(scan.finished_at)}</td>
                            </tr>
                        ))}
                    </tbody>


                </Table>
                

            </Sheet>
        </div>
    );
}

export default Scans;