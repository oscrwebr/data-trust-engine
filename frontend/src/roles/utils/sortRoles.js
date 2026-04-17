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
    }   

    return sortedRoles;
}