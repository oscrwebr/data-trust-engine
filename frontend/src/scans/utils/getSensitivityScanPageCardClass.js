// Function dynamically renders different classes for the scan page cards on the sensitivity page
// Would be better if I was able to take into the length of each file rather than setting arbitrary thresholds
export const getSensitivityScanPageCardClass = (detections, totalFiles) => {

    if(detections ==  0) {
        return "clean";
    }

    // Each file has a threshold of 50 detections
    // E.g. If there are 4 files then the threshold for 'critical' would be 200 detections
    const threshold = totalFiles * 50;

    if(detections >= threshold) {
        return "critical";
    }

    return "issues";
}