import { PiTrashBold } from "react-icons/pi";
import { PiFileBold } from "react-icons/pi";
import { useNavigate } from "react-router-dom";
import api from "../api/axiosConfig";
import { useState } from "react";


function DuplicatePopUpCard({duplicate}) {

    const navigate = useNavigate();

    const[deleteSuccess, setDeleteSuccess] = useState(false);
    const[deleteError, setDeleteError] = useState(false);

    async function handleDelete(event) {
        event.stopPropagation();

        try {
            await api.delete("/ingestion/delete-file", {
                params: {
                    graph_id: duplicate.graph_file_id
                 }
             });
            setDeleteSuccess(true);
            // Hides success message after 6 seconds
            setTimeout(() => setDeleteSuccess(false), 6000);
            console.log("File deleted successfully");
            window.location.reload();
            
            
        }
        catch (error) {
            setDeleteError(true);
            // Hides error message after 6 seconds
            setTimeout(() => setDeleteError(false), 6000);
            console.error("Error deleting file:", error);
            console.error("duplicate:", duplicate);
        }
    }

    return (
        <div className="duplicate-popup-card">
            <div className="duplicate-popup-card-row">
                {/* <PiFileBold className="duplicate-popup-card-icon" /> */}
                <span className="duplicate-popup-card-name">{duplicate.file_name}</span>

                <div className="duplicate-popup-card-buttons">
                    <button className="duplicate-popup-card-button delete"
                        onClick={handleDelete}
                    >
                        <PiTrashBold size={20} className="duplicate-popup-card-button-icon" />
                        <span>Delete</span>
                    </button>
                    <button className="duplicate-popup-card-button view-file" onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/files/${duplicate.file_id}`);
                    }}>
                        <PiFileBold size={20} className="duplicate-popup-card-button-icon" />
                        <span>View</span>
                    </button>
                </div>
                <div className="duplicate-popup-card-message">
                    {deleteSuccess && (
                        <span className="duplicate-delete-success">Duplicate successfully deleted!</span>
                    )}
                    {deleteError && (
                        <span className="duplicate-delete-error">Error deleting file.</span>
                    )}
                </div>
            </div>

            
        </div>
    )

}

export default DuplicatePopUpCard;