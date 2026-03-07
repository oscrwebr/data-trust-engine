import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext";
import { Message } from "primereact/message";
import { Toast } from 'primereact/toast';
import axios from 'axios';
import { Dialog } from "primereact/dialog";

import FileUpload from "./FileUpload.jsx";
import styles from "./CreateWorkspace.module.css";



function CreateWorkspace({toast}) {
  const visible = true;
  const [name, setName] = useState(null);
  const [file, setFile] = useState([]);
  const navigate = useNavigate();

  const [nameError, setNameError] = useState(false);
  const [imageError, setImageError] = useState(false);

   useEffect(() => {
    if (file){
      setImageError(false);
    }
    }, [file]);
  

  const showMessage = () => {
      toast.current.show({ severity: 'success', summary: 'Success', detail: 'Workspace successfully created!', life: 4000});
  };

  const handleCreateWorkspace = async () => {
    
    try {
      let image = null;
      if(file.length > 0){
        const base64 = await toBase64(file[0]);
        image = base64.split(",")[1];
      }
      
      const response = await axios.post("http://localhost:8000/workspace/create-workspace", {
        name: name || null,
        image: image,
      });

      if(response.data == "name"){
        setNameError(true);
        setImageError(false);
      } else if (response.data == "image"){
        setNameError(false);
        setImageError(true);
      } else {
        showMessage();
        navigate("/dashboard");
        setNameError(false);
        setImageError(false);
        
      }

    } catch (error) {
      console.log(error)
    }
  }

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });

  return (
    <div>
        <Dialog
          className={styles.cw_dialog}
          visible={visible}
          header={<h2 className={styles.cw_dialog_header}>Create Your Workspace</h2>}
          draggable={false}
          >
          <div>
            <div className={styles.cw_input_container}>
              <label className={styles.cw_label_name}>Workspace Name</label>
              <InputText id={styles.cw_workspace_name} className={`mr-2 ${nameError ? "p-invalid" : ""}`} placeholder="Enter workspace name" value={name} onChange={(e) => setName(e.target.value)}/>
               {nameError &&(<Message severity="error" className={styles.cw_error} text={<p className={styles.cw_error_text}>You must give your workspace a name.</p>}/>)}
              <label className={styles.cw_label_image}>Upload Workspace Image</label>
              <FileUpload file={file} setFile={setFile}/>
               {imageError &&(<Message severity="error" className={styles.cw_error} text={<p className={styles.cw_error_text}>You must upload your workspace's image.</p>}/>)}
              <Button onClick={handleCreateWorkspace} data-testid="send-invite-button" id={styles.cw_create_workspace}>Create Workspace</Button>
            </div>
          </div>
        </Dialog>
    </div> 
  );
}

export default CreateWorkspace;