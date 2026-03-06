import {React, useState} from 'react';
import { useDropzone } from 'react-dropzone';

import styles from "./CreateWorkspace.module.css";

function FileUpload() {
    const [file, setFile] = useState([]);
    const { getRootProps, getInputProps } = useDropzone({
        onDrop: (acceptedFiles) => {
            if (acceptedFiles.length > 1) {
                return;
            } else {
                setFile(acceptedFiles[0])
            }
        },
    });

    return (
        <div className={styles.cw_container}>
            <div {...getRootProps()} className={styles.cw_file_input}>
                <input {...getInputProps()} />
                <div className={styles.cw_upload_container}>
                    <i id={styles.cw_upload_icon} className="pi pi-download"></i>
                    <p><strong>Choose a file</strong> or drag it here</p>
                </div>
            </div>
            <div>
                {file.map((f) => (
                <FileCard
                  name={f.name}  
                />
            ))}

            </div>
        </div>
    );
}

export default FileUpload;