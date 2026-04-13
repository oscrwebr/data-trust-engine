import { useEffect, useState} from 'react';
import { useDropzone } from 'react-dropzone';
import FileCard from './FileCard.jsx';

import styles from "./CreateWorkspace.module.css";

function FileUpload({file, setFile, error, setError}) {
    const { getRootProps, getInputProps } = useDropzone({
        maxFiles: 1,
        onDrop: (acceptedFiles) => {setFile(acceptedFiles)}
    });

    const regex = /\.(png|jpg|jpeg|webp|heic)$/i;

    useEffect(() => {
        if (file.length > 0) {
            const fileName = file[0].name;

            if (!regex.test(fileName)) {
                setError(true);
                setFile([]);
            } else {
                setError(false);
            }
        }
    }, [file])

    return (
        <div className={styles.cw_container} data-testid="file-upload">
            <div {...getRootProps()} className={styles.cw_file_input}>
                <input {...getInputProps()} />
                <div className={styles.cw_upload_container}>
                    <i id={styles.cw_upload_icon} className="pi pi-download"></i>
                    <p><strong>Choose a file</strong> or drag it here</p>
                </div>
            </div>
            {error == false && (<div>
                {file.map((f, index) => (
                    <FileCard 
                        key={index} 
                        file={f} 
                        onRemove={() => setFile([])} 
                    />
                ))}
            </div>)}
        </div>
    );
}

export default FileUpload;