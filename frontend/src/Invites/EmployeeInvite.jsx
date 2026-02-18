import "primereact/resources/themes/lara-light-indigo/theme.css"; 
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

import styles from "./EmployeeInvite.module.css";
import { useState } from "react";

import { InputText } from "primereact/inputtext";
import { InputTextarea} from "primereact/inputtextarea"
import { Calendar } from 'primereact/calendar';
import { Dialog } from "primereact/dialog";
import { Button } from "primereact/button";

function EmployeeInvite({ visible, setVisible }) {

  const [expiryDate, setExpiryDate] = useState(null);
  const today = new Date();
  const maxDay = new Date();
  maxDay.setMonth(maxDay.getMonth() + 1);

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
        <p className={styles.d_description}>Send an invite to an employee by specifying their email address. You can also set an optional message and expiry date for the invitation.</p>
        
        <div className={styles.d_email_container}>
            <small id="email-address">
                Enter your employee's email address
            </small>
            <InputText id="email-address" aria-describedby="email-address" className={styles.d_email_input} placeholder="Email address"/>
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
            <small id="text-area">
                Attach a customised message to your invite
            </small>
            <InputTextarea 
                id="text-area" 
                className={styles.d_textarea_input} 
                maxLength={100} 
                rows={9} 
                placeholder="Hi [Employee Name], &#10;&#10;You have been invited to join our system. Please use the link below to activate your account before the expiry date. If you have any questions, feel free to reach out. &#10;&#10;Best regards, &#10;&#10;[Admin Name]"/>
        </div>
        <Button>Send Invite <i style={{ marginLeft: 10}} className="pi pi-send"></i></Button>
      </Dialog>
    </div>
  );
}

export default EmployeeInvite;