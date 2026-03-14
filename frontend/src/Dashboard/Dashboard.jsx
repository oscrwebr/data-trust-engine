import Invite from "../invites/invites";
import { Button } from "primereact/button";
import { useState, useEffect, useRef } from "react";
import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { Badge } from "primereact/badge"
import { Toast } from "primereact/toast"
import Notification from "../components/notifications/Notification.jsx";

function Dashboard({toast}) {
  const [visible, setVisible] = useState(false);
  const [user, setUser] = useState({});
  const [notifications, setNotifications] = useState([])
  const toastNotifications = useRef(null);

  const notificationCount = notifications.length;

  let displayValue = '';

  if (notificationCount === 0) {
    displayValue = ''; 
  } else if (notificationCount > 5) {
    displayValue = '5+'; 
  } else {
    displayValue = notificationCount;
  }

  useEffect(() => {
      api.get("/workspace/dashboard")
      .then(res => {
          console.log(res)
          if (res.data.user) {
              setUser(res.data.user);
          }
      })
      .catch(error => console.log(error))

      api.get("/workspace/get-notifications")
      .then(res => {
          setNotifications(res.data)
      })
      .catch(error => console.log(error))
  }, []);

  function handleNotifications(){
    notifications.forEach(notification => {
      toastNotifications.current.show({
        severity: 'info', 
        summary: notification.title, 
        detail: notification.body,  
        sticky: true, 
        content: (props) => (
          <Notification 
            key={notification.id}
            title={notification.title}
            body={notification.body}
            date={notification.datetime}
          />
        )
      });
    });
  }

  return (
    <div>
        <div className={styles.header}>
          <h1>Dashboard</h1>
          <Button id={styles.bell_btn} onClick={handleNotifications} text 
            style={{marginRight: 50, background: "transparent", border: "none", boxShadow: "none", outline: "none"}}
          ><i className="pi pi-bell p-overlay-badge" style={{ fontSize: 21}}><Badge value={displayValue} severity="danger"></Badge></i></Button>
        </div>
        <Button onClick={() => setVisible(true)}>Invite Employee</Button>
        <Invite visible={visible} setVisible={setVisible} toast={toast}/>
        <Toast ref={toastNotifications} position="bottom-center" onRemove={() => toastRef.current.clear()} />
    </div>
  );
}

export default Dashboard;