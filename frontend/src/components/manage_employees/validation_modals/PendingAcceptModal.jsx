import { Dialog } from "primereact/Dialog"
import { Button } from "primereact/button";
import styles from "./modal.module.css"

function PendingAcceptModal({email, visible, setVisible, onRemove}) {
    
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
                    <span>Are you sure you want to accept <br/><strong>{email}</strong> into your workspace?</span>
                    <div className={styles.button_container}>
                        <Button className={styles.remove_button} onClick={onRemove}>Yes, accept employee</Button>
                        <Button className={styles.cancel_button} onClick={setVisible}>Cancel</Button>
                    </div>
                </div>
            </Dialog>
        </div>
    )
}

export default PendingAcceptModal;

