// Helper function to use across application
export const formatDateTime = (dateTimeString) => {
            // Format date into dd/mm/yyyy, hh:mm:ss
            // For ongoing scans... Display "-" as the Finished At time
            if (!dateTimeString) {
                return "-";
            }
            const date = new Date(dateTimeString);
            const formattedDate = date.toLocaleDateString("en-GB");
            const formattedTime = date.toLocaleTimeString("en-GB");
            return `${formattedDate}, ${formattedTime}`;
    }