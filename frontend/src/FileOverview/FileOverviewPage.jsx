import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import FileScanHistoryItem from "./FileScanHistoryItem";
import LatestScanResultCard from "./LatestScanResultCard";
import EmployeeAccessItem from "./EmployeeAccessItem";
import styles from "./FileOverview.module.css";

import { FaRegFileAlt, FaEdit, FaHashtag } from "react-icons/fa";
import { FaShieldAlt } from "react-icons/fa";
import { FaHistory } from "react-icons/fa";
import { FaUserFriends } from "react-icons/fa";

import api from "../api/axiosConfig"


function FileOverviewPage({toast}) {
    const { file_id } = useParams();
    const backend_uri = import.meta.env.VITE_BACKEND_HOST || "http://localhost:8000"

    const [file, set_file] = useState(null);
    const [file_scans_history, set_file_scans_history] = useState(null);
    const [latest_scan_results, set_latest_scan_results] = useState(null);
    const [employees_with_access, set_employees_with_access] = useState([]);

    const [loading, set_loading] = useState(true);

    useEffect(() => {
        const fetch_file = async() => {
            try {
                const file_response = await fetch(`${backend_uri}/scanning/get_file/${file_id}`);
                const file_data = await file_response.json()

                const file_scans_history_response = await fetch(`${backend_uri}/scanning/get_file_scans/${file_id}`)
                const file_scans_history_data = await file_scans_history_response.json()

                const latest_scan_results_response = await fetch(`${backend_uri}/scanning/get_file_latest_scan_results/${file_id}`)
                const latest_scan_results_data = await latest_scan_results_response.json()

                const employees_with_access_response = await fetch(`${backend_uri}/access_mapping/get_file_employees_with_access/${file_id}`)
                const employees_with_access_data = await employees_with_access_response.json()

                set_file(file_data)
                set_file_scans_history(file_scans_history_data)
                set_latest_scan_results(latest_scan_results_data)
                set_employees_with_access(employees_with_access_data)

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

    const handleSendEmail = (id) => {
        const user = employees_with_access.find(
            employee => employee.user_id === id
        );

        api.post("/access_mapping/send-violations-email", {
            file_name: file.file_name,
            employee: user
        }).then(res => {
            if(res.data == "cooldown"){
                showErrorMessage();
            } else {
                showSuccessMessage();
            }
        })
    }

    const grouped_latest_scan_results = (latest_scan_results || []).reduce((acc, item) => {
        if (!acc[item.category]) {
            acc[item.category] = [];
        }

        acc[item.category].push(item);
        return acc;
    }, {});

    const showSuccessMessage = () => {
        toast.current.show({ severity: 'info', summary: 'Info', detail: 'An email containing the violations was sent to the employee.', life: 4000});
    };

    const showErrorMessage = () => {
        toast.current.show({ severity: 'error', summary: 'Error', detail: 'You are sending this employee too many emails, please try again later.', life: 4000});
    };

    const formatted_date = (value) => {
        return new Date(value).toLocaleString("en-GB", {
            day: "numeric",
            month: "long",
            year: "numeric",
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
        });
    };

    return (
        <div className={styles.file_overview_page}>
            <div className={styles.file_header_card}>
                <div className={styles.file_header_top}>
                    <div className={styles.file_icon}>
                        <FaRegFileAlt />
                    </div>

                    <h1 className={styles.file_name}>
                        {file.file_name}
                    </h1>
                </div>

                <div className={styles.file_metadata}>
                    <div className={styles.metadata_chip}>
                        <FaHistory className={styles.metadata_icon} />
                        <div>
                            <div className={styles.metadata_label}>Last Scanned</div>
                            <div className={styles.metadata_value}>
                                {file.last_scanned ? formatted_date(file.last_scanned) : "Not scanned yet"}
                            </div>
                        </div>
                    </div>

                    <div className={styles.metadata_chip}>
                        <FaEdit className={styles.metadata_icon} />
                        <div>
                            <div className={styles.metadata_label}>Last Modified</div>
                            <div className={styles.metadata_value}>
                                {file.last_modified ? formatted_date(file.last_modified) : "Unknown"}
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div className={styles.file_overview_content}>
                <div className={styles.file_overview_main_column}>
                    <div className={styles.latest_scan_results_container}>
                        <div className={styles.section_title}>
                            <FaShieldAlt className={styles.section_icon}/>
                            <h2 className={styles.latest_scan_results_title}>Latest Scan Results</h2>
                        </div>

                        {Object.entries(grouped_latest_scan_results).map(([category, results]) => (
                            <div key={category} className={styles.latest_scan_category_section}>
                                <h3 className={styles.latest_scan_category_title}>{category}</h3>

                                <div className={styles.latest_scan_results_list}>
                                    {results.map((result, index) => (
                                        <LatestScanResultCard key={index} result={result} />
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className={styles.scan_history_container}>
                        <div className={styles.section_title}>
                            <FaHistory className={styles.section_icon}/>
                            <h2 className={styles.scan_history_title}>Scan History</h2>
                        </div>

                        <div className={styles.scan_history_list}>
                            {file_scans_history.map((scan) => (
                                <FileScanHistoryItem key={scan.scan_id} scan={scan} />
                            ))}
                        </div>
                    </div>
                </div>

                <div className={styles.file_overview_sidebar}>
                    <div className={styles.employees_with_access_container}>
                        <div className={styles.section_title}>
                            <FaUserFriends className={styles.section_icon}/>
                            <h2 className={styles.employees_with_access_category_title}>Employees With Access</h2>
                        </div>

                        {employees_with_access.length === 0 ? (
                            <p>No employees with access found.</p>
                        ) : (
                            employees_with_access.map((employee) => (
                                <EmployeeAccessItem
                                    key={employee.user_id}
                                    employee={employee}
                                    sendEmail={(value) => handleSendEmail(value)}
                                />
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
} 


export default FileOverviewPage;