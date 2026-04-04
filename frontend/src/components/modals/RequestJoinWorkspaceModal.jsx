import styles from "../manage_employees/validation_modals/modal.module.css"
import { useState } from "react";

import { IconField } from "primereact/iconfield";
import { InputText } from "primereact/inputtext";
import { InputIcon } from "primereact/inputicon";
import { Dialog } from "primereact/Dialog"
import { Button } from "primereact/button";

function RequestJoinWorkspaceModal({visible, setVisible}) {
    const [searchValue, setSearchValue] = useState(null)

    return(
        <div>
            <Dialog
                className={styles.request_dialog}
                visible={visible} 
                onHide={setVisible}
                header={<h1 className={styles.dialog_header}>Request to Join a Workspace</h1>}
                draggable={false}
                dismissableMask={true}
                >
                
                <div className={styles.container}>
                    <span>Browse available workspaces below and send a request to join.</span>
                    <IconField iconPosition="left">
                        <InputIcon className="pi pi-search"></InputIcon>
                        <InputText onChange={(e) => setSearchValue(e.target.value)} style={{ width: '23vw'}} placeholder="Search available workspaces" className="p-inputtext-sm"/>
                    </IconField>
                    <strong>Selected Workspace</strong>
                    <Button>Send Request</Button>
                </div>
            </Dialog>
        </div>
    )
}

export default RequestJoinWorkspaceModal;

