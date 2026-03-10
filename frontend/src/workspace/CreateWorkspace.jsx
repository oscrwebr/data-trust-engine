import React, { useState, useRef, useEffect } from "react";
import api from "../api/axiosConfig.js";
import { useNavigate } from "react-router-dom";

import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext";
import { Message } from "primereact/message";
import { Dialog } from "primereact/dialog";

import FileUpload from "./FileUpload.jsx";
import styles from "./CreateWorkspace.module.css";



function CreateWorkspace({toast}) {
  const visible = true;
  const [name, setName] = useState(null);
  const [file, setFile] = useState([]);
  const navigate = useNavigate();
  const formData = new FormData();
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
      formData.append(
        "name",
        name && !["null", "undefined"].includes(name) ? name : ""
      );

      if (file[0]) {
        formData.append("image", file[0]);
      }

      const response = await api.post("/workspace/create-workspace", formData);

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

  return (
    <div>
        <Dialog
          className={styles.cw_dialog}
          visible={visible}
          header={<h2 className={styles.cw_dialog_header}>Create Your Workspace</h2>}
          draggable={false}
          closable={false}
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