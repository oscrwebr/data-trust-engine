// Function that helps change the default subcategory text to user friendly format
// If new subcategories are added in future they will need to be added here too

export const formatSubcategoryText = (subcategory) => {
    switch (subcategory) {
        case "NAME":
            return "Contains names";
        case "PHONE":
            return "Contains phone numbers";
        case "EMAIL":
            return "Contains email addresses";
        case "ADDRESS":
            return "Contains personal addresses";
        case "POSTCODE":
            return "Contains postcodes";
        case "IBAN":
            return "Contains bank account information";
        case "VAT":
            return "Contains VAT information";
        case "CITATION":
            return "Contains citations";
        case "ACT":
            return "Contains acts";
        case "REGULATION":
            return "Contains regulations";
        case "CASE_NAME":
            return "Contains case names";
        default:
            return `Contains ${subcategory.toLowerCase()}`;
    }
}