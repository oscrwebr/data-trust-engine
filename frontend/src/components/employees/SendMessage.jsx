import styles from "./employees.module.css";
import { Chip } from 'primereact/chip';
import { Dialog } from "primereact/dialog";
import { InputTextarea } from 'primereact/inputtextarea';
    
function SendMessage({visible, setVisible, selectedEmployees, onRemove}) {

    return (
        <div>
            <Dialog
                className={styles.dialog}
                visible={visible} 
                onHide={() => {setVisible(false)}}
                header={<h1 className={styles.dialog_header}>Send your employees a message</h1>}
                draggable={false}
                dismissableMask
            >
                <span>Send a message to the employees defined below. You can remove recipients by clicking the <i className="pi pi-times-circle"/> button</span><br/><br/>
                <strong>Selected Recipients</strong>
                <div className={styles.chip_container}> 
                    {selectedEmployees.map((employee) => (
                        <div className={styles.chip}>
                            <span style={{ marginRight: '5px' }}>{employee.user.firstname} {employee.user.surname}</span>
                            <i id={styles.chip_remove_icon} onClick={() => onRemove(employee.user.user_id)} className="pi pi-times-circle"/>
                        </div>
                    ))}
                </div>
                <div>
                    <strong>Enter your Message</strong>
                    <div style={{ marginTop:'5px'}} className="card flex justify-content-center">
                        <InputTextarea rows={3} cols={49} maxLength='140' placeholder="Enter the message you would like to send" style={{ resize: 'none', fontSize: '15px' }}/>
                    </div>
                </div>
            </Dialog>
        </div>
    )
}

export default SendMessage;