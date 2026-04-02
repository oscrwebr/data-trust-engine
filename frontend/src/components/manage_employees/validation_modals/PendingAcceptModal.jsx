import { Dialog } from "primereact/Dialog"
import { Button } from "primereact/button";
import styles from "./modal.module.css"

function PendingAcceptModal({email, visible, setVisible, onAccept}) {
    
    return(
        <div>
            <Dialog
                className={styles.dialog}
                visible={visible} 
                draggable={false}
                dismissableMask={true}
                closable={false}    
                >
                
                <div className={styles.modal_container}>
                    <i id={styles.info_icon} className="pi pi-exclamation-circle"/>
                    <span>To accept this employee, an email containing an invite request will be sent to <strong>{email}</strong>.</span>
                    <div className={styles.button_container}>
                        <Button className={styles.remove_button} onClick={onAccept}>Yes, accept employee</Button>
                        <Button className={styles.cancel_button} onClick={setVisible}>Cancel</Button>
                    </div>
                </div>
            </Dialog>
        </div>
    )
}

export default PendingAcceptModal;

