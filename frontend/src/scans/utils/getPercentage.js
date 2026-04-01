export const getPercentage = (number, totalFiles) => {
    if (totalFiles === 0) return 0;

    return Math.round((number / totalFiles) * 100);
}