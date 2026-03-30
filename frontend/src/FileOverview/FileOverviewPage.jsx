import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import FileScanHistoryItem from "./FileScanHistoryItem";
import LatestScanResultCard from "./LatestScanResultCard";
import styles from "./FileOverview.module.css";


function FileOverviewPage() {
    const { file_id } = useParams();

    const [file, set_file] = useState(null);
    const [file_scans_history, set_file_scans_history] = useState(null);
    const [latest_scan_results, set_latest_scan_results] = useState(null);

    const [loading, set_loading] = useState(true);

    useEffect(() => {
        const fetch_file = async() => {
            try {
                const file_response = await fetch(`http://localhost:8000/scanning/get_file/${file_id}`);
                const file_data = await file_response.json()

                const file_scans_history_response = await fetch(`http://localhost:8000/scanning/get_file_scans/${file_id}`)
                const file_scans_history_data = await file_scans_history_response.json()

                const latest_scan_results_response = await fetch(`http://localhost:8000/scanning/get_file_latest_scan_results/${file_id}`)
                const latest_scan_results_data = await latest_scan_results_response.json()

                set_file(file_data)
                set_file_scans_history(file_scans_history_data)
                set_latest_scan_results(latest_scan_results_data)

            } catch (error) {
                console.error("Error while fetching file data:", error)

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

            <div className={styles.latest_scan_results_container}>
                <h2 className={styles.latest_scan_results_title}>Latest Scan Results</h2>

                <div className={styles.latest_scan_results_list}>
                    {latest_scan_results.map((result, index) => (
                        <LatestScanResultCard key={index} result={result} />
                    ))}
                </div>
            </div>

            <div className={styles.scan_history_container}>
                <h2 className={styles.scan_history_title}>Scan History</h2>

                <div className={styles.scan_history_list}>
                    {file_scans_history.map((scan) => (
                        <FileScanHistoryItem key={scan.scan_id} scan={scan} />
                    ))}
                </div>
            </div>
        </div>
    );
} 


export default FileOverviewPage;