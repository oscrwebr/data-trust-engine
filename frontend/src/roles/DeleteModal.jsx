import styles from "./delete_modal.module.css"
import { Dialog } from "primereact/dialog";
import { Button } from "primereact/button";

function DeleteModal({visible, setVisible, onRemove}){
    return (
        <div>
            <Dialog
                className={styles.dialog}
                visible={visible} 
                onHide={setVisible}
                draggable={false}
                dismissableMask={true}
                closable={false}    
                >
                
                <div className={styles.modal_container}>
                    <i id={styles.info_icon} className="pi pi-exclamation-circle"/>
                    <span>Are you sure you want to delete this role?</span>
                    <div className={styles.button_container}>
                        <Button className={styles.remove_button} onClick={onRemove}>Yes, delete role</Button>
                        <Button className={styles.cancel_button} onClick={setVisible}>Cancel</Button>
                    </div>
                </div>
            </Dialog>
        </div>
    )
}

export default DeleteModal;