// Different to GetScanPageCardClass as this is for the 'Clean Files' card which needs different thresholds
export const getCleanFilesClass = (percentage) => {

    if(percentage >= 75) {
        return "clean";
    }

    if (percentage >= 50) {
        return "issues";
    }
    
    return "critical";

}