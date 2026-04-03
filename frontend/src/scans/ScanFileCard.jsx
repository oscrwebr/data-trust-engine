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

    console.log(scan_file);


    return (
        <div className={`scan-page-file-card ${cardClass}`}>
            <p>{scan_file.file_name}</p>
        </div>
    )
}

export default ScanFileCard;