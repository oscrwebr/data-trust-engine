export const formatSubcategoryName = (subcategory) => {
    switch (subcategory) {
        case "NAME":
            return "Names";
        case "PHONE":
            return "Phone Numbers";
        case "EMAIL":
            return "Email Addresses";
        case "ADDRESS":
            return "Addresses";
        case "POSTCODE":
            return "Postcodes";
        case "IBAN":
            return "Bank Account Numbers";
        case "VAT":
            return "VAT Numbers";
        case "CITATION":
            return "Citations";
        case "ACT":
            return "Acts";
        case "REGULATION":
            return "Regulations";
        case "CASE_NAME":
            return "Case Names";
        default:
            return `Contains ${subcategory.toLowerCase()}`;
    }
}