import { PiFileBold } from "react-icons/pi";
import { PiTextAaBold } from "react-icons/pi";
import { PiCardsBold } from "react-icons/pi";
import { PiCheckCircleBold } from "react-icons/pi";
import ScanFileCard from "./ScanFileCard";
import { getScanPageCardClass } from "./utils/getScanPageCardClass";
import { getPercentage } from "./utils/getPercentage";
import { getCleanFilesClass } from "./utils/getCleanFilesClass";
import { formatNamingConventionName } from "./utils/formatNamingConventionName";

function OrganisationScanPage({ scan }) {


    
    const namingIssues = scan.files.filter(
        // A file is only considered to have a naming issue if it fails ALL naming convention checks
        // .every() checks for this (see below)
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/every
        file => file.naming_convention_scan_results.every(result => !result.passed)
    ).length;

    // Similar to the hash check in the backend (duplicate_scan function in scanning/service.py)
    // Groups files together by their duplicate_group_id
    const duplicateGroups = {}

    for (const file of scan.files) {
        // Skip files without a duplicate group (not duplicates)
        // Continues the for loop
        if (file.duplicate_group_id === null) {
            continue
        }
        // Create an empty array if it hasn't been created yet
        if (!duplicateGroups[file.duplicate_group_id]) {
            duplicateGroups[file.duplicate_group_id] = [];
        }
        // Add the file to that group
        duplicateGroups[file.duplicate_group_id].push(file);
    }

    // Loop to count the number of files within a duplicate group
    let duplicateCount = 0;
    for (const duplicateGroupId in duplicateGroups) {
        // -1 so if there is two files in one duplicate group it only counts as 1 duplicate file
        // Makes more sense than saying there are 2 duplicates
        duplicateCount += duplicateGroups[duplicateGroupId].length - 1;
    }

    // Get the amount of issues and percentage of clean files for display
    const totalIssues = namingIssues + duplicateCount;
    const cleanFiles = scan.file_count - totalIssues;
    const cleanFilesPercentage = getPercentage(cleanFiles, scan.file_count);

    

    return (
        <>
        {/* To change the colour of a card, apply either 'critical' 'issues' or 'clean' to the scan-page-card class */}
        <div className="scan-page-card-container">
            <div className="scan-page-card">
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Total Files</span>
                    <span className="scan-page-card-title">{scan.file_count}</span>
                    
                </div>
                <div>
                    <div className="icon-box">
                    <PiFileBold size={30}/>
                    </div>
                </div>
            </div>
            <div className={`scan-page-card ${getScanPageCardClass(namingIssues, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Naming Issues</span>
                    {/* HARDCODED FOR NOW */}
                    <span className="scan-page-card-title">{namingIssues}</span>
                    
                </div>
                <div>
                    <div className="icon-box">
                    <PiTextAaBold size={30}/>
                    </div>
                </div>
            </div>
            <div className={`scan-page-card ${getScanPageCardClass(duplicateCount, scan.file_count)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Duplicate Files</span>
                    <span className="scan-page-card-title">{duplicateCount}</span>
                    
                </div>
                <div>
                    <div className="icon-box">
                    <PiCardsBold size={30}/>
                    </div>
                </div>
            </div>
            <div className={`scan-page-card ${getCleanFilesClass(cleanFilesPercentage)}`}>
                <div className="scan-page-card-text">
                    <span className="scan-page-card-subtitle">Clean Files</span>
                    <span className="scan-page-card-title">{cleanFilesPercentage}%</span>
                    
                </div>
                <div className="scan-page-card-image">
                    <div className="icon-box">
                    <PiCheckCircleBold size={30}/>
                    </div>
                </div>
            </div>
            
        </div>
        <h2 className="scan-page-files-heading">All Scanned Files</h2>

        <div className="scan-page-file-container">
            {scan.files.map(scan_file => (
                <ScanFileCard key={scan_file.scan_file_id} scan_file={scan_file} scan_type={scan.scan_type} scan_files={scan.files} />
            ))}
        </div>
        </>
        

    )
}

export default OrganisationScanPage;