// Sort games based on selected sorting option
export const sortRoles = (rolesToSort, sortOption) => {
    const sortedRoles = [...rolesToSort];

    switch (sortOption) {
        case "nameAscending":
            // https://www.w3schools.com/jsref/jsref_localecompare.asp
            sortedRoles.sort((a, b) => a.name.localeCompare(b.name));
            break;

        case "nameDescending":
            sortedRoles.sort((a, b) => b.name.localeCompare(a.name));
            break;

        case "newestToOldest":
            sortedRoles.sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated));
            break;

        case "oldestToNewest":
            sortedRoles.sort((a, b) => new Date(a.last_updated) - new Date(b.last_updated));
            break;
    }   

    return sortedRoles;
}