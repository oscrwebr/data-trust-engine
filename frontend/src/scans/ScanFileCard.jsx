import { PiWarningCircle } from "react-icons/pi";
import { PiCheckCircle } from "react-icons/pi";
import { formatNamingConventionName } from "./utils/formatNamingConventionName";
import { formatSubcategoryText } from "./utils/formatSubcategoryText";
import { PiMagnifyingGlassBold } from "react-icons/pi";
import { useNavigate } from "react-router-dom";
import { PiCopySimpleBold } from "react-icons/pi";
import { useState } from "react";
import DuplicatePopUp from "./DuplicatePopUp";





function ScanFileCard({scan_file, scan_type, scan_files}) {

    const navigate = useNavigate();

    const [showPopUp, setShowPopup] = useState(false);

    const duplicateFiles = scan_file.duplicate_group_id ?
                            scan_files.filter(file => 
                            // Check for scan files with the same duplicate group id
                            file.duplicate_group_id === scan_file.duplicate_group_id 
                            // Don't display the scanned file as a duplicate of itself in the pop up (only want other files)
                            && file.scan_file_id !== scan_file.scan_file_id)
                        // Check whether the file has a duplicate group (first line), otherwise return an empty array
                        : [];
            

    const issues = []
    // Issue check for organisational scan files
    if(scan_type === "organisation") {

        // Files are considered to have naming issues if they fail ALL checks (same logic to work out total naming issues of a scan)
        const passedCheck = scan_file.naming_convention_scan_results.every(result => !result.passed);

        if (passedCheck) {
            // Add issue details to the array
            issues.push({
                type: "Naming Issue",
                naming_convention: scan_file.naming_convention_scan_results.map(result => result.naming_convention_name),
                suggested_name: scan_file.naming_convention_scan_results.map(result => result.suggested_name)
            });
        }

        if (scan_file.duplicate_group_id != null) {
            issues.push({
                type: "Duplicate File"
            })
        }
        
    }

    if (scan_type === "sensitivity") {
        // For each category issue that the file has, add the category and subcategory to the issues array
        scan_file.sensitivity_scan_results.forEach(result => {
            issues.push({
                category: result.category,
                subcategory: result.subcategory_name,
                highRisk: result.is_high_risk
            })
        })
        
    }

    const detectionCount = scan_file.detection_count

    const isHighRisk = issues.some(issue => issue.highRisk);

    const cardClass = issues.length === 0 ?
        "card-clean" :
        isHighRisk ? "card-critical" :
        "card-issue";

    const issueCheck = issues.length === 0;

    // Get the text to show for each scan file card (can show multiple types of issues e.g. Naming Issue, Duplicate)
    const scanFilePillText = issueCheck 
                            ? 'Clean' : 
                            scan_type === "organisation"
                            ? issues.map(i => i.type).join(", ")
                            : `${detectionCount} Detections Found`
                            

    return (
        <>
        <div className={`scan-page-file-card ${cardClass} scan-page-link-fix`} onClick={() => navigate(`/files/${scan_file.file_id}`)}>
            <div className="scan-file-top">
                <div className="scan-file-top-left">
                    {issueCheck ? (
                        <PiCheckCircle size={26} className="scan-file-icon icon-clean" />
                    ) : (
                        <PiWarningCircle size={26} className={`scan-file-icon ${isHighRisk ? 'critical-issue' : 'icon-issue'}`} />
                    )}
                    <span className={`scan-file-pill ${issueCheck ? 'pill-clean' : isHighRisk ? 'pill-critical' : 'pill-issue'}`}>
                        {scanFilePillText}
                    </span>


                </div>
            </div>

            <div className="scan-file-name">
                <span>{scan_file.file_name}</span>
            </div>
            {scan_type === "organisation" && issues.length > 0 && (
                <div className="scan-file-details-wrapper">
                    {issues.map((issue, index) => (
                        <div key={index} className="scan-file-details">
                            {issue.type === "Naming Issue" && (
                                <>
                                <div className="scan-file-issue">
                                    <div className="scan-file-issue-text-heading">
                                        <span>Issue:</span>
                                    </div>
                                    <div className="scan-file-issue-text">
                                        <span>Name does not follow: {issue.naming_convention.map(formatNamingConventionName).join(", ")}</span>
                                    </div>
                                </div>

                                <div className="scan-file-suggested">
                                    <div className="scan-file-suggested-heading">
                                        <span>Suggested Name:</span>
                                    </div>
                                    <div className="scan-file-suggested-text">
                                        <span>{issue.suggested_name[0]}</span>
                                    </div>
                                </div>
                                </>
                                    
                            )}

                            {issue.type === "Duplicate File" && (
                                <>
                                <div className="scan-file-issue">
                                    <div className="scan-file-issue-text-heading">
                                        <span>Issue:</span>
                                    </div>
                                    <div className="scan-file-issue-text">
                                        <span>File is a duplicate</span>
                                    </div>
                                </div>

                                <div className="scan-file-suggested">
                                    <div className="scan-file-duplicates-heading">
                                        <span>Manage Duplicates</span>
                                    </div>
                                    <button className="duplicate-scan-file-button"
                                    // Link inside a link code adapted from: 
                                    // https://stackoverflow.com/a/30362416
                                    // Opens pop up to view duplicate files related to the scanned file
                                            onClick={(event) => {event.preventDefault(); event.stopPropagation(); setShowPopup(true)}}
                                    >
                                        <PiCopySimpleBold /> View Duplicates
                                    </button>
                                </div>
                                </>
                            )}

                        </div>
                    ))}

                </div>
                
            )}


            {scan_type === "sensitivity" && issues.length > 0 && (
                <>
                <div className="scan-file-sensitivity-details">
                    <div className="scan-file-issue-text-heading">
                        <span>Detections:</span>
                    </div>
                    {issues.map((issue, index) => (
                        <div key={index} className={`sensitivity-detection ${issue.highRisk ? 'high-risk' : 'standard-risk'}`}>
                            <div className="sensitivity-detection-category">
                                <span>{issue.category}</span>
                            </div>
                            <div className="sensitivity-detection-subcategory">
                                <span>{formatSubcategoryText(issue.subcategory)}</span>
                            </div>
                        </div>
                    ))}

                </div>
                <div className="sensitivity-scan-file-view-details">
                    <button className="sensitivity-scan-file-button"
                    // Link inside a link code adapted from: 
                    // https://stackoverflow.com/a/30362416
                            onClick={(event) => {event.preventDefault(); event.stopPropagation(); navigate(`/scan-file/${scan_file.scan_file_id}`)}}
                    >
                        <PiMagnifyingGlassBold /> View Advanced Details
                    </button>
                </div>
                </>
            )}

        </div>

        {showPopUp && (
            <DuplicatePopUp duplicates={duplicateFiles} onClose={() => setShowPopup(false)} />
        )}
        </>
    )
}

export default ScanFileCard;