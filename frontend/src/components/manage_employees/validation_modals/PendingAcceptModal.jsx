import { Dialog } from "primereact/Dialog"
import { Button } from "primereact/button";
import styles from "./modal.module.css"
import dayjs from "dayjs";

function PendingAcceptModal({email, visible, setVisible, onAccept, date}) {
    
    const d = dayjs(date);
    const expiry = d.format("D MMMM YYYY");

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
                    <span>An email containing an invite request will be sent to <strong>{email}</strong>. It will expiry on the {expiry}.</span>
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

