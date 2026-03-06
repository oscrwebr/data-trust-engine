import { useEffect, useState } from "react";

import styles from "./CreateWorkspace.module.css";
import { Button } from "primereact/button";

function FileCard({file, onRemove}){

    const [preview, setPreview] = useState(null);

    useEffect(() => {
        if (!file) return;

        if (file.type.startsWith("image/")) {
            const objectUrl = URL.createObjectURL(file);
            setPreview(objectUrl);

            return () => URL.revokeObjectURL(objectUrl);
        }
    }, [file]);

    return (
        <div className={styles.f_container}>
            {preview ? (
                <img src={preview} alt={file.name} className={styles.f_image_preview} />
            ) : (
                <div><i className="pi pi-image"></i></div>
            )}
            <p><strong>{file.name}</strong></p>
            <Button onClick={onRemove} className={styles.f_remove_button} icon="pi pi-times-circle" text/>
        </div>
    )
}
  
export default FileCard;