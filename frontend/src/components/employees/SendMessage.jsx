import styles from "./employees.module.css";
import { useState } from "react";

import { Dialog } from "primereact/dialog";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { MultiSelect } from "primereact/multiselect"
import { IconField } from "primereact/iconfield";
import { InputTextarea } from 'primereact/inputtextarea';
        



function SendMessage({visible, setVisible, roles, setRoles}) {
    const [searchValue, setSearchValue] = useState([])
    const [chips, setChips] = useState([])
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
                <span>Search for employees by name or email. You can also choose roles and risk levels to quickly target multiple recipients.</span><br/><br/>
                <strong>Select Recipients</strong>
                <div className={styles.dialog_input_container}>
                    <IconField iconPosition="left">
                        <InputIcon className="pi pi-search"> </InputIcon>
                        <InputText onChange={(e) => setSearchValue(e.target.value)} style={{ width: '14vw', marginRight: '10px'}} placeholder="Search employees" className="p-inputtext-sm"/>
                    </IconField>
                    <div className="card flex justify-content-center" style={{ marginRight: '10px' }}>
                        <MultiSelect options={roles} onChange={(e) => setChips(e.value)} optionLabel="name" style={{ fontSize:'14px', height: '40px' }} placeholder="Roles"/>
                    </div>
                    <div className="card flex justify-content-center">
                        <MultiSelect optionLabel="name" onChange={(e) => setChips(e.value)} style={{ fontSize:'14px', height: '40px' }} placeholder="Risk Levels"/>
                    </div>
                </div>
                <div>
                    <strong>Enter your Message</strong>
                    <div style={{ marginTop:'5px'}} className="card flex justify-content-center">
                        <InputTextarea rows={3} cols={49} maxLength='140' placeholder="Enter the message you would like to send" style={{ resize: 'none' }}/>
                    </div>
                </div>
            </Dialog>
        </div>
    )
}

export default SendMessage;