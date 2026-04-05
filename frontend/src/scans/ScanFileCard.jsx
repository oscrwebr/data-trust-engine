import { PiWarningCircle } from "react-icons/pi";
import { PiCheckCircle } from "react-icons/pi";
import { formatNamingConventionName } from "./utils/formatNamingConventionName";
import { Link } from "react-router-dom";


function ScanFileCard({scan_file, scan_type}) {

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
        
    }

    const cardClass = issues.length === 0 ?
        "card-clean" :
        "card-issue";

    const issueCheck = issues.length === 0;

    // Get the text to show for each scan file card (can show multiple types of issues e.g. Naming Issue, Duplicate)
    const scanFilePillText = issueCheck ? 'Clean' : issues.map(i => i.type).join(", ");;

    return (
        <Link to={`/file/${scan_file.file_id}`} className="scan-page-link-fix">
        <div className={`scan-page-file-card ${cardClass}`}>
            <div className="scan-file-top">
                <div className="scan-file-top-left">
                    {issueCheck ? (
                        <PiCheckCircle size={26} className="scan-file-icon icon-clean" />
                    ) : (
                        <PiWarningCircle size={26} className="scan-file-icon icon-issue" />

                    )}

                    <span className={`scan-file-pill ${issueCheck ? 'pill-clean' : 'pill-issue'}`}>
                        {scanFilePillText}
                    </span>


                </div>
            </div>

            <div className="scan-file-name">
                <span>{scan_file.file_name}</span>
            </div>
            {issues.length > 0 && (
                <div>
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

                        </div>
                    ))}

                </div>
                
            )}

        </div>
        </Link>
    )
}

export default ScanFileCard;