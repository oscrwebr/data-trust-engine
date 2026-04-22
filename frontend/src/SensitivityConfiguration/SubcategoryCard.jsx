import {PiUser,PiPhone,PiEnvelope,PiMapPin,PiHash,PiBank,PiPercent,PiScales,PiGavel,PiBookOpen,PiFileText, } from "react-icons/pi";
import { PiReceipt } from "react-icons/pi";
import { PiMailbox } from "react-icons/pi";

import { formatSubcategoryName } from "./utils/formatSubcategoryName";

function SubcategoryCard({ subcategory, isHigh, onClick }) {

    const subcategoryIcons = {
        "NAME": <PiUser size={22}/>,
        "PHONE": <PiPhone size={22}/>,
        "EMAIL": <PiEnvelope size={22}/>,
        "ADDRESS": <PiMapPin size={22}/>,
        "POSTCODE": <PiMailbox size={22}/>,          
        "IBAN": <PiBank size={22}/>,
        "VAT": <PiReceipt size={22}/>,           
        "CITATION": <PiScales size={22}/>,        
        "ACT": <PiGavel size={22}/>,              
        "REGULATION": <PiBookOpen size={22}/>,   
        "CASE_NAME": <PiFileText size={22}/>,     
    };

    return (
        <div className="subcategory-card">
            <div className="subcategory-card-left">
                <div className="subcategory-pill">
                    <div className="subcategory-icon-box">
                        {subcategoryIcons[subcategory.subcategory_name.toUpperCase()]}
                    </div>

                    <div className="subcategory-name">
                        <span>{formatSubcategoryName(subcategory.subcategory_name)}</span>
                    </div>
                </div>
            </div>

            
        </div>
    )

}

export default SubcategoryCard;