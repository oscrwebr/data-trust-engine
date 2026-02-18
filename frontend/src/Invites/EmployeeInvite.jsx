import "primereact/resources/themes/lara-light-indigo/theme.css"; 
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

import styles from "./EmployeeInvite.module.css";
import { use, useState } from "react";

import { InputText } from "primereact/inputtext";
import { Calendar } from 'primereact/calendar';
import { Dialog } from "primereact/dialog";
import { Button } from "primereact/button";

import axios from 'axios';

function EmployeeInvite({ visible, setVisible }) {
  const [expiryDate, setExpiryDate] = useState(null);
  const [email, setEmail] = useState(null);

  const today = new Date();
  const maxDay = new Date();
  maxDay.setMonth(maxDay.getMonth() + 1);

  const handleSendInvite = async () => {
    try {
      await axios.post("http://localhost:8000/invite/send-invite", {
        email: email,
        expiry_date: expiryDate ? expiryDate.toISOString() : null,
      });
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div>
      <Dialog 
        className={styles.d_dialog}
        visible={visible} 
        onHide={() => setVisible(false)}
        header={<h2 className={styles.d_dialog_header}>Send your employee an invite</h2>}
        draggable={false}
        dismissableMask
        >
        <p className={styles.d_description}>Send an invite to an employee by specifying the recipient's email address. You can also set an expiry date for the invitation.</p>
        
        <div className={styles.d_email_container}>
            <small id="email-address">
                Enter your employee's email address
            </small>
            <InputText id="email-address" aria-describedby="email-address" className={styles.d_email_input} placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)}/>
            <small id="expiry-date">
                Select an expiry date for the invite
            </small>
            <Calendar
                id="expiry-date"
                className={styles.d_date_input}
                showIcon
                minDate={today}    
                maxDate={maxDay} 
                value={expiryDate} onChange={(e) => setExpiryDate(e.value)} dateFormat="dd/mm/yy" 
            />
        </div>
        <Button onClick={() => handleSendInvite()}>Send Invite <i style={{ marginLeft: 10}} className="pi pi-send"></i></Button>
      </Dialog>
    </div>
  );
}

export default EmployeeInvite;