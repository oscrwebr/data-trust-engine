import DuplicatePopUpCard from "./DuplicatePopUpCard";
import "./popup.css"

function DuplicatePopUp({scan_file, duplicates, onClose}) {

    const duplicateCount = duplicates.length

    return (
        // Closing pop up when clicking outside the pop up window adapted from:
        // https://stackoverflow.com/a/70612838
        <div className="popup-wrapper" onClick={onClose}>
            <div className="popup-window" onClick={(e) => e.stopPropagation()}>
                <div className="popup-header">
                    <div className="popup-header-top">
                        <span className="popup-file-name">{scan_file.file_name}</span>
                    </div>

                    <div className="popup-file-hash">
                        <span className="popup-hash-label">Hash</span>
                        <span className="popup-hash-value">{scan_file.hash}</span>
                    </div>
                </div>

                <span className="popup-duplicates-heading">Duplicate Files ({duplicateCount})</span>

                {duplicates.map((duplicate) => (
                    <DuplicatePopUpCard key={duplicate.scan_file_id} duplicate={duplicate} />
                ))}



            </div>
        </div>
    )
}

export default DuplicatePopUp;