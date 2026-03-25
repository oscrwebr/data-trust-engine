import Invite from "../invites/invites";
import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { Toast } from "primereact/toast";
import { useOutletContext } from "react-router-dom";

function Dashboard({toast}) {

  const { toastNotifications, visible, setVisible, setNotifications } = useOutletContext();

  // Function to handle removing notifications
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
        <h1 data-testid="dashboard-h1">Dashboard</h1>
        <Invite className={styles.d_invite_dialog} visible={visible} setVisible={setVisible} toast={toast}/>

        {/* This is how and where the notifications are loaded */}
        <Toast className={styles.d_toast} ref={toastNotifications} onRemove={(message) => handleRemove(message.id)} position="top-right" />
    </div>
  );
}

export default Dashboard;