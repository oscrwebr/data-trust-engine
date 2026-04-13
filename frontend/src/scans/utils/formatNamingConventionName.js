export function formatNamingConventionName(name) {
    // Naming convention names currently get sent in snake case (pascal_case, snake_case etc.)
    // This turns these names into a more readable format (Pascal Case, Snake Case)

    return name.split("_").map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");
}