import { PiFileBold } from "react-icons/pi";
import { PiTextAaBold } from "react-icons/pi";
import { PiCardsBold } from "react-icons/pi";
import { PiCheckCircleBold } from "react-icons/pi";




function OrganisationScanPage({ scan }) {
    return (
        // To change the colour of a card, apply either 'issues' or 'clean' to the scan-page-card class
        <div className="scan-page-card-container">
            <div className="scan-page-card">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Total Files Scanned</span>
                    <span className="scan-page-card-title">{scan.file_count}</span>
                    
                </div>
                <div>
                    <PiFileBold size={50}/>
                </div>
            </div>
            <div className="scan-page-card issues">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Naming Issues</span>
                    {/* HARDCODED FOR NOW */}
                    <span className="scan-page-card-title">7</span>
                    
                </div>
                <div>
                    <PiTextAaBold size={50}/>
                </div>
            </div>
            <div className="scan-page-card clean">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Duplicate Files</span>
                    <span className="scan-page-card-title">0</span>
                    
                </div>
                <div>
                    <PiCardsBold size={50}/>
                </div>
            </div>
            {/* need to create function to calculate % */}
            <div className="scan-page-card clean">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Clean Files</span>
                    <span className="scan-page-card-title">87%</span>
                    
                </div>
                <div>
                    <PiCheckCircleBold size={50}/>
                </div>
            </div>
            
        </div>
    )
}

export default OrganisationScanPage;