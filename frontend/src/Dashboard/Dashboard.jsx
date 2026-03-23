import Invite from "../invites/invites";
import { useState, useEffect, useRef } from "react";
import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { Toast } from "primereact/toast"
import Notification from "../components/notifications/Notification.jsx";
import Header from "../components/header/header.jsx";
import Sidebar from "../components/navbar/Sidebar.jsx";

function Dashboard({toast}) {
  const [visible, setVisible] = useState(false);
  const [sidebarVisible, setSidebarVisible] = useState(true)
  const [user, setUser] = useState({});
  const [workspace, setWorkspace] = useState(null)
  const [notifications, setNotifications] = useState([])
  const toastNotifications = useRef(null);

  useEffect(() => {
      api.get("/workspace/dashboard")
      .then(res => {
          if (res.data.user) {
            setUser(res.data.user);
            console.log(res.data.user)
            setWorkspace(res.data.workspace);
          }
      })
      .catch(error => console.log(error))

      api.get("/workspace/get-notifications")
        .then(res => {
            setNotifications(res.data)
        })
        .catch(error => console.log(error))
  }, []);

  const handleRemove = async (id) => {
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
          <Sidebar setSidebarVisible={setSidebarVisible} firstname={user.firstname} surname={user.surname} setVisible={setVisible} role={user.role}/>
        </div>)}
        
        <div className={styles.main}>
          <Header firstname={user.firstname} lastname={user.surname} workspace={workspace} sidebarVisible={sidebarVisible} setSidebarVisible={setSidebarVisible} toastRef={toastNotifications} notifications={notifications} setNotifications={setNotifications}/>
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