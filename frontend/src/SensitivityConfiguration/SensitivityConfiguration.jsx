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

    const handleClick = async (subcategory_id, is_high) => {
        try {
            // Add configuration to DB
            await api.post("/scanning/update_workspace_detection_sensitivity", {
                sensitivity_subcategory_id: subcategory_id,
                is_high: is_high
            });

            // Update UI rather than refreshing to see changes
            setCategories(prevCategories => prevCategories.map(category => ({
                ...category,
                subcategories: category.subcategories.map(subcategory => 
                    subcategory.subcategory_id === subcategory_id
                    ? { ...subcategory, is_high_risk: is_high }
                    : subcategory
                )
            })));
        }
        catch (error) {
            console.error("Error updating sensitivity categories:", error);
        }
    }

    if (loading) {
        return (
            <>
            {/* Heading area rendered as well*/}
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
            {/* Heading area rendered as well */}
            <div className="scan-header">
                <h1 className="scan-heading">
                    Sensitivity Categories
                </h1>
            <Divider/>
            </div>
            <p className="scan-loading">Error loading sensitivity categories.</p>
            </>
        )
    }

    const categoryIcons = {
            "PERSONAL": <PiUserListBold size={30} />,
            "LEGAL CASE": <PiScalesBold size={30} />,
            "FINANCIAL": <PiCurrencyGbpBold size={30}/>
        }


    return (
        <div className="page">
        <div>
            <div className="scan-header">
                <div className="header_container">
                    <i id="header_icon" className="pi pi-search"/>
                    <h1 className="title">Detection Sensitivity</h1>
                </div>
            <Divider/>
            </div>
        </div>
        {categories.map(({category, subcategories}) => (
            <div key={category}>
                {/* Each category has a header */}
                <div className="category-header">
                    <span>{category} Detections</span>
                </div>
                <div className="subcategory-card-container">
                    {/* Map each subcategory into a card */}
                    {subcategories.map((subcategory) => (
                        <SubcategoryCard key={subcategory.subcategory_id} subcategory={subcategory} isHigh={subcategory.is_high_risk} onClick={handleClick}/>
                    ))}
                </div>
            </div>
        ))}
        </div>
    )
}

export default SensitivityConfiguration;