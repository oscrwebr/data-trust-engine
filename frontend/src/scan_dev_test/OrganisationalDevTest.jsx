import api from "../api/axiosConfig";

function OrganisationalDevTest() {
    const performScan = async () => {
        try {
            await api.post("/scanning/organisation_scan", {
                naming_convention_ids: [2]
            });
            console.log("Organisation scan performed successfully");
        } catch (error) {
            console.error("Error performing organisation scan:", error);
        }
    }

    return (
        <div>
            <h1>FOR DEV PURPOSES...</h1>
            <button style={{color: 'white'}} onClick={performScan}>Perform Organisation Scan</button>
        </div>
    )
}

export default OrganisationalDevTest;