import { React, useState } from "react";

import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext";
import { Toast } from 'primereact/toast';
import { Dialog } from "primereact/dialog";

import styles from "./CreateWorkspace.module.css";

function CreateWorkspace() {
  const visible = true;
  const [name, setName] = useState(null);

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
              <label className={styles.cw_label}>Workspace Name</label>
              <InputText className={styles.cw_workspace_name} placeholder="Enter workspace name" value={name} onChange={(e) => setName(e.target.value)}/>

              <label className={styles.cw_label}>Upload Image</label>

              <Button data-testid="send-invite-button" id={styles.cw_create_workspace}>Create Workspace</Button>
            </div>
          </div>
        </Dialog>
    </div> 
  );
}

export default CreateWorkspace;