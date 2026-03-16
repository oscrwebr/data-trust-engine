import {React, useState} from 'react';
import { useDropzone } from 'react-dropzone';
import FileCard from './FileCard.jsx';

import styles from "./CreateWorkspace.module.css";

function FileUpload({file, setFile}) {
    const { getRootProps, getInputProps } = useDropzone({
        maxFiles: 1,
        onDrop: (acceptedFiles) => {setFile(acceptedFiles)}
    });

    return (
        <div className={styles.cw_container} data-testid="file-upload">
            <div {...getRootProps()} className={styles.cw_file_input}>
                <input {...getInputProps()} />
                <div className={styles.cw_upload_container}>
                    <i id={styles.cw_upload_icon} className="pi pi-download"></i>
                    <p><strong>Choose a file</strong> or drag it here</p>
                </div>
            </div>
            <div>
                {file.map((f, index) => (
                    <FileCard 
                    key={index} 
                    file={f} 
                    onRemove={() => setFile([])} 
                    />
                ))}
            </div>
        </div>
    );
}

export default FileUpload;