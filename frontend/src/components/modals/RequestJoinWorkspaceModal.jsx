import styles from "../manage_employees/validation_modals/modal.module.css"
import api from "../../api/axiosConfig"
import { useState, useEffect } from "react";
import { Dialog } from "primereact/Dialog"
import { Button } from "primereact/button";
import { Dropdown } from "primereact/dropdown";

import WorkspaceOptionTemplate from "../workspace/WorkspaceOptionTemplate"

function RequestJoinWorkspaceModal({toast, visible, setVisible}) {
    const [workspaces, setWorkspaces] = useState([])
    const [selectedWorkspace, setSelectedWorkspace] = useState(null)
    const title = "New Invite Request"
    const body = "An employee has requested join your workspace. You can review this request in Manage Employees."

    useEffect(() => {
        api.get("/workspace/get-all-workspaces")
        .then(res => {
            setWorkspaces(res.data)
        })
    }, [])

    const showRequestSentSuccess = () => {
      toast.current.show({ severity: 'success', summary: 'Success', detail: 'Invite request sent!', life: 4000});
    };

    const handleRequestJoinWorkspace = () => {
        api.post("/workspace/request-join-workspace", {
            title: title,
            body: body,
            workspace_id: selectedWorkspace.id,
        })
        .then(res => {
            showRequestSentSuccess();
            setVisible(false);
        })
    }

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
                    <div className="card flex justify-content-center">
                        <Dropdown value={selectedWorkspace} onChange={(e) => setSelectedWorkspace(e.value)} options={workspaces} placeholder="Select a Workspace" 
                            filter filterDelay={400} valueTemplate={(workspace) => (<WorkspaceOptionTemplate workspace={workspace} />)} itemTemplate={(workspace) => (<WorkspaceOptionTemplate workspace={workspace} />)} className="w-full md:w-14rem" />
                    </div>    
                    
                    <Button onClick={() => handleRequestJoinWorkspace()}>Send Request</Button>
                </div>
            </Dialog>
        </div>
    )
}

export default RequestJoinWorkspaceModal;

