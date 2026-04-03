import { Dialog } from "primereact/Dialog"
import { Button } from "primereact/button";
import styles from "../manage_employees/validation_modals/modal.module.css"

function RequestJoinWorkspaceModal({visible, setVisible}) {
    
    return(
        <div>
            <Dialog
                className={styles.dialog}
                visible={visible} 
                onHide={setVisible}
                draggable={false}
                dismissableMask={true}
                >
                
                <div className={styles.container}>
                </div>
            </Dialog>
        </div>
    )
}

export default RequestJoinWorkspaceModal;

