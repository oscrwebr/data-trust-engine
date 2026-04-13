import "./popup.css"

function DuplicatePopUp({duplicates, onClose}) {
    return (
        // Closing pop up when clicking outside the pop up window adapted from:
        // https://stackoverflow.com/a/70612838
        <div className="popup-wrapper" onClick={onClose}>
            <div className="popup-window" onClick={(e) => e.stopPropagation()}>
                <h1>Duplicate Files</h1>
            </div>
        </div>
    )
}

export default DuplicatePopUp;