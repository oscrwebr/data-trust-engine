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
  const [isNotificationsVisible, setIsNotificationsVisible] = useState(false); // State to track visibility
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
        console.log(res)
        setNotifications(res.data)
      })
      .catch(error => console.log(error))
  }, []);

  function handleNotifications(){
    setIsNotificationsVisible((prev) => !prev);
    if (!isNotificationsVisible) {
      notifications.forEach(notification => {
      toastNotifications.current.show({
        id: notification.id,
        severity: 'info', 
        sticky: true, 
        closable: true,
        content: (props) => (
          <Notification 
            key={notification.id}
            title={notification.title}
            body={notification.body}
            date={notification.datetime}
          />
        ),
      });
    });
    } else {
      toastNotifications.current.clear();
    }
  }

  const handleRemove = async (id) => {
    console.log(id)
    try {
      await api.post("/workspace/delete-notification", {
        notification_id: id, 
      })
      
      setNotifications((prev) => prev.filter(n => n.id !== id));

    } catch (error){
      console.log(error)
    }
  }

  return (
    <div>
        <div className={styles.header}>
          <h1>Dashboard</h1>
          <Button id={styles.bell_btn} onClick={handleNotifications} text 
            style={{marginRight: 50, background: "transparent", border: "none", boxShadow: "none", outline: "none"}}
          ><i className="pi pi-bell p-overlay-badge" style={{ fontSize: 21}}>{notificationCount > 0 && <Badge value={displayValue} severity="danger" />}</i></Button>
        </div>
        <Button onClick={() => setVisible(true)}>Invite Employee</Button>
        <Invite visible={visible} setVisible={setVisible} toast={toast}/>
        <Toast className={styles.d_toast} ref={toastNotifications} onRemove={(message) => handleRemove(message.id)} position="top-right" />
    </div>
  );
}

export default Dashboard;