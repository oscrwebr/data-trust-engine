import { PiTrashBold } from "react-icons/pi";
import { PiFileBold } from "react-icons/pi";


function DuplicatePopUpCard({duplicate}) {

    return (
        <div className="duplicate-popup-card">
            <div className="duplicate-popup-card-row">
                {/* <PiFileBold className="duplicate-popup-card-icon" /> */}
                <span className="duplicate-popup-card-name">{duplicate.file_name}</span>

                <div className="duplicate-popup-card-buttons">
                    <button className="duplicate-popup-card-button delete">
                        <PiTrashBold size={20} className="duplicate-popup-card-button-icon" />
                        <span>Delete</span>
                    </button>
                    <button className="duplicate-popup-card-button view-file">
                        <PiFileBold size={20} className="duplicate-popup-card-button-icon" />
                        <span>View</span>
                    </button>
                </div>
            </div>

            
        </div>
    )

}

export default DuplicatePopUpCard;