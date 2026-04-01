export const getPercentage = (number, total) => {
    if (total === 0) return 0;

    return Math.round((number / total) * 100);
}