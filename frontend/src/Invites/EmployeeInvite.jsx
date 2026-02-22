import "primereact/resources/themes/lara-light-indigo/theme.css"; 
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

import styles from "./EmployeeInvite.module.css";
import { useState, useRef } from "react";

import { InputText } from "primereact/inputtext";
import { IconField } from "primereact/iconfield";
import { Toast } from 'primereact/toast';
import { InputIcon } from "primereact/inputicon";
import { Calendar } from 'primereact/calendar';
import { Message } from 'primereact/message';
import { Dialog } from "primereact/dialog";
import { Button } from "primereact/button";

import axios from 'axios';

function EmployeeInvite({ visible, setVisible }) {
  const [expiryDate, setExpiryDate] = useState(null);
  const [email, setEmail] = useState(null);
  const [email_error, setEmailError] = useState(false);
  const [date_error, setDateError] = useState(false);
  const [email_valid, setEmailValid] = useState(false);
  const toast_success = useRef(null);

  const showMessage = () => {
      toast_success.current.show({ severity: 'success', summary: 'Success', detail: 'Invite successfully sent!', life: 4000});
  };

  const today = new Date();
  const maxDay = new Date();
  maxDay.setMonth(maxDay.getMonth() + 1);

  const handleSendInvite = async () => {
    try {
      const response = await axios.post("http://localhost:8000/invite/send-invite", {
        email: email || null,
        expiry_date: expiryDate ? expiryDate.toISOString() : null,
      });
      
      if(response.data.success == "invalid"){
        setEmailError(true);
        setDateError(false);
        setEmailValid(false);

      } else if (response.data.success == "expiry") {
        setDateError(true);
        setEmailError(false);
        setEmailValid(true)
        
      } else if (response.data.success) {
        showMessage(toast_success);
        setDateError(false);
        setEmailError(false);
        setEmailValid(true);
        setVisible(false);
        setEmail(null);
        setExpiryDate(null);
        setEmailValid(false);
      }
 
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div>
      <Toast ref={toast_success} position="top-right" />
      <Dialog 
        className={styles.d_dialog}
        visible={visible} 
        onHide={() => {setVisible(false), setEmail(null), setExpiryDate(null), setEmailValid(false)}}
        header={<h2 className={styles.d_dialog_header}>Send your employee an invite</h2>}
        draggable={false}
        dismissableMask
        >
        <p className={styles.d_description}>Send an invite to an employee by specifying the recipient's email address. You can also set an expiry date for the invitation.</p>
        
        <div className={styles.d_container}>
          <div className={styles.d_input_container}>
            <small id="email-address">
                Enter your employee's email address
            </small>
            <IconField iconPosition="right" className={styles.d_icon_field}>
                {email_valid ? (<InputIcon data-testid="email-valid-icon" id={styles.d_check_icon} className="pi pi-check-circle" />) : (<span/>)}
                <InputText id={styles.d_email_address} aria-describedby="email-address" className={`mr-2 ${email_error ? "p-invalid" : ""}`} placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)}/>
            </IconField>
            {email_error &&(<Message severity="error" className={styles.d_error} text={<p className={styles.d_error_text}>This email address doesn't exist</p>}/>)}
         
            <small id="expiry-date" className={styles.d_expiry_date}>
                Select an expiry date for the invite
            </small>
            <Calendar
              id={styles.d_date_input}
              className={`mr-2 ${date_error ? "p-invalid" : ""}`}
              showIcon
              minDate={today}    
              maxDate={maxDay} 
              value={expiryDate} onChange={(e) => setExpiryDate(e.value)} dateFormat="dd/mm/yy" 
            />
            {date_error &&(<Message severity="error" className={styles.d_error} text={<p className={styles.d_error_text}>No expiry date selected</p>}/>)}
            <Button onClick={() => handleSendInvite()} data-testid="send-invite-button" id={styles.d_send_button}>Send Invite <i style={{ marginLeft: 10}} className="pi pi-send"></i></Button>
          </div>
        </div>
      </Dialog>
    </div>
  );
}

export default EmployeeInvite;