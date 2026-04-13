import { getPercentage } from "./getPercentage";

// Function to determine what colour each scan page card should show
// Depends on the percentage of issues found in the scan
// E.g. If 50% of files contain naming convention issues then it would display the 'critical' class
export const getScanPageCardClass = (number, totalFiles) => {
    const percentage = getPercentage(number, totalFiles);

    if(percentage >= 50) {
        return "critical";
    }

    if (percentage >= 20) {
        return "issues";
    }
    
    return "clean";

}