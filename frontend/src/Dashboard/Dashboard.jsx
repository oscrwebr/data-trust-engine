import Invite from "../invites/invites";
import { Button } from "primereact/button";
import { useState, useEffect, useRef } from "react";
import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { Toast } from "primereact/toast"
import Notification from "../components/notifications/Notification.jsx";
import Header from "../components/header/header.jsx";
import AdminNavbar from "../components/navbar/AdminNavbar.jsx";

function Dashboard({toast}) {
  const [visible, setVisible] = useState(false);
  const [sidebarVisible, setSidebarVisible] = useState(true)
  const [user, setUser] = useState({});
  const [workspace, setWorkspace] = useState(null)
  const [notifications, setNotifications] = useState([])
  const toastNotifications = useRef(null);
  const [isNotificationsVisible, setIsNotificationsVisible] = useState(false);
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
          if (res.data.user) {
            setUser(res.data.user);
            setWorkspace(res.data.workspace);
            console.log(res.data.user)
            console.log(res.data.workspace)
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
    <div className={styles.container}>
        {sidebarVisible &&(<div className={styles.navbar_container}>
          <AdminNavbar setSidebarVisible={setSidebarVisible} firstname={user.firstname} surname={user.surname} setVisible={setVisible}/>
        </div>)}
        
        <div className={styles.main}>
          <Header firstname={user.firstname} lastname={user.surname} workspace={workspace} sidebarVisible={sidebarVisible} setSidebarVisible={setSidebarVisible}/>
          <div className={styles.content}>
            <h1>Dashboard</h1>
            <Invite className={styles.d_invite_dialog} visible={visible} setVisible={setVisible} toast={toast}/>
            <Toast className={styles.d_toast} ref={toastNotifications} onRemove={(message) => handleRemove(message.id)} position="top-right" />
          </div>
        </div>
    </div>
  );
}

export default Dashboard;