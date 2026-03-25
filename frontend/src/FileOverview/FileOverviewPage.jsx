import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";


function FileOverviewPage() {
    const { file_id } = useParams();

    const [file, set_file] = useState(null);
    const [loading, set_loading] = useState(true);

    useEffect(() => {
        const fetch_file = async() => {
            try {
                const file_response = await fetch(`http://localhost:8000/scanning/get_file/${file_id}`);
                const file_data = await file_response.json()

                const scan_history_response = await fetch(`http://localhost:8000/scanning/get_file_scans/${file_id}`)

                set_file(file_data)
            } catch (error) {
                console.error("Error while fetching file:", error)
            } finally {
                set_loading(false);
            }
        };

        fetch_file();
    }, [file_id]);

    if (loading) return <p>File loading...</p>

    if (!file) return <p>File not found.</p>

    return (
        <div>
            <h1>{file.file_name}</h1>
            <p>Hash: {file.hash}</p>


            <h2>Scan History</h2>
        </div>
    );
} 


export default FileOverviewPage;