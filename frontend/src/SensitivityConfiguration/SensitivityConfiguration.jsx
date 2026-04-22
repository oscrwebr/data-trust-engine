import api from "../api/axiosConfig";
import { useState, useEffect } from "react";
import "../scans/scans.css";
import { Divider } from "primereact/divider";
import { PiUserListBold, PiScalesBold, PiCurrencyGbpBold } from "react-icons/pi";
import "./sensitivity.css"
import SubcategoryCard from "./SubcategoryCard";

function SensitivityConfiguration() {

    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get("/scanning/get_sensitivity_categories")
            .then(response => {
                setCategories(response.data)
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching sensitivity categories:", error);
                setError(error);
                setLoading(false);
            })
    }, [])

    if (loading) {
        return (
            <>
            <div className="scan-header">
                <h1 className="scan-heading">
                    Sensitivity Categories
                </h1>
            <Divider/>
            </div>
            <p className="scan-loading">Loading sensitivity categories...</p>
            </>
        )
    }

    if (error) {
        return (
            <>
            <div className="scan-header">
                <h1 className="scan-heading">
                    Sensitivity Categories
                </h1>
            <Divider/>
            </div>
            <p className="scan-loading">Error loading sensitivity categories: {error.message}</p>
            </>
        )
    }

    const categoryIcons = {
            "PERSONAL": <PiUserListBold size={30} />,
            "LEGAL CASE": <PiScalesBold size={30} />,
            "FINANCIAL": <PiCurrencyGbpBold size={30}/>
        }


    return (
        <>
        <div>
            <div className="scan-header">
                <h1 className="detection-heading">
                    Detection Sensitivity
                </h1>
            <Divider/>
            </div>
        </div>
        {categories.map(({category, subcategories}) => (
            <div key={category}>
                <div className="category-header">
                    <span>{category} Detections</span>
                </div>
                <div className="subcategory-card-container">
                    {subcategories.map((subcategory) => (
                        <SubcategoryCard key={subcategory.subcategory_id} subcategory={subcategory} />
                    ))}
                </div>
            </div>
        ))}
        </>
    )
}

export default SensitivityConfiguration;