import { Button } from "primereact/button";
import styles from "./employees.module.css";
import { Dialog } from "primereact/dialog";
import { InputTextarea } from 'primereact/inputtextarea';
import api from "../../api/axiosConfig";
import { useState } from "react";

function SendMessage({visible, setVisible, selectedEmployees, setSelectedEmployees, onRemove, toast}) {
    const [text, setText] = useState(null)
    
    const showSuccessMessage = () => {
      toast.current.show({ severity: 'success', summary: 'Success', detail: 'Message successfully sent!', life: 4000});
    };

    const showErrorMessage = () => {
        toast.current.show({ severity: 'error', summary: 'Error', detail: 'You cannot send a message without a body.', life: 4000});
    };

    const handleSendMessage = async () => {
        try {
            await api.post("/workspace/send-message", {
                employees: selectedEmployees.map(emp => emp.user.user_id),
                body: text
            }).then(res => {
                if(res.data == true){
                    showSuccessMessage();
                    setVisible(false);
                    setSelectedEmployees([]);
                    setText(null)
                } else {
                    showErrorMessage();
                }
            })
        } catch (error) {
            console.log(error)
        }
    }

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
                        <InputTextarea onChange={(e) => setText(e.target.value)} rows={3} cols={49} maxLength='140' placeholder="Enter the message you would like to send" style={{ resize: 'none', fontSize: '15px' }}/>
                    </div>
                </div>
                <Button onClick={handleSendMessage} className={styles.send_message_button}>Send Message</Button>
            </Dialog>
        </div>
    )
}

export default SendMessage;