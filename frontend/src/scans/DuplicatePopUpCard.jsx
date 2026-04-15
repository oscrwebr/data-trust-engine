function DuplicatePopUpCard({duplicate}) {

    return (
        <div className="duplicate-popup-card">
            <div className="duplicate-popup-card-top">
                {/* <PiFileBold className="duplicate-popup-card-icon" /> */}
                <span className="duplicate-popup-card-name">{duplicate.file_name}</span>
            </div>
        </div>
    )

}

export default DuplicatePopUpCard;