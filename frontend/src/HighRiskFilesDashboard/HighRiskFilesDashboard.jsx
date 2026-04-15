import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import HighRiskFileRow from "./HighRiskFileRow";

import styles from "./HighRiskFilesDashboard.module.css";
import { FaShieldAlt } from "react-icons/fa";

function HighRiskFilesDashboard() {
    const [files, set_files] = useState([]);
    const [loading, set_loading] = useState(true);
    const [error, set_error] = useState(true);

    const backend_uri = import.meta.env.VITE_BACKEND_HOST || "http://localhost:8000"

    const navigate = useNavigate();

    useEffect(() => {
        const fetch_high_risk_files = async() => {
            try {
                // Set loading to true every time method called
                set_loading(true);
                set_error(null);

                const files_response = await fetch(`${backend_uri}/access_mapping/get_highest_risk_files`);
                const files_data = await files_response.json();

                set_files(files_data);
            } catch (error) {
                set_error("Failed to load high risk files.")
            } finally {
                set_loading(false)
            }
        }

        fetch_high_risk_files();
    }, []);

    if (loading) return <p>High risk files loading...</p>

    if (error) return <p>Error: {error}</p>

    return (
        <div className={styles.high_risk_files_page}>
            <div className={styles.high_risk_files_header}>
                <div className={styles.title_row}>
                    <FaShieldAlt className={styles.title_icon}/>
                    <h1 className={styles.page_title}>High-Risk Files Dashboard</h1>
                </div>
                <p className={styles.page_subtitle}>Your organisation's files ranked by access risk and sensitivity detections</p>
            </div>

            <div className={styles.high_risk_files_table}>
                <div className={styles.high_risk_files_table_header}>
                    <div>Risk</div>
                    <div>File Name</div>
                    <div>Employees with Access</div>
                    <div>Valid Access</div>
                    <div>Detections</div>
                    <div></div>
                </div>

                {files.length > 0 ? (
                    files.map((file) => (
                        <HighRiskFileRow key={file.file_id}file={file}/>
                    ))
                ) : (
                    <div className={styles.empty_state}>
                        No high-risk files found.
                    </div>
                )}
            </div>
        </div>
    )
}


export default HighRiskFilesDashboard;