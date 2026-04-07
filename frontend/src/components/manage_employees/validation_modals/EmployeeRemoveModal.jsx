import { Dialog } from "primereact/dialog"
import { Button } from "primereact/button";
import styles from "./modal.module.css"

function EmployeeRemoveModal({firstname, surname, visible, setVisible, onRemove}) {
    
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
                    <span>Are you sure you want to remove <br/><strong>{firstname} {surname}</strong> from your workspace?</span>
                    <div className={styles.button_container}>
                        <Button className={styles.remove_button} onClick={onRemove}>Yes, remove employee</Button>
                        <Button className={styles.cancel_button} onClick={setVisible}>Cancel</Button>
                    </div>
                </div>
            </Dialog>
        </div>
    )
}

export default EmployeeRemoveModal;

