import Invite from "../invites/invites";
import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { Toast } from "primereact/toast";
import { useOutletContext } from "react-router-dom";
import { useState } from "react";
import { Button } from "primereact/button";
import RequestJoinWorkspaceModal from "../components/modals/RequestJoinWorkspaceModal.jsx";

function Dashboard({toast}) {

  const { toastNotifications, visible, setVisible, setNotifications, user, workspace } = useOutletContext();
  const [requestJoinWorkspaceVisible, setRequestJoinWorkspaceVisible] = useState(false);
  
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
        <Invite className={styles.d_invite_dialog} visible={visible} setVisible={setVisible} toast={toast}/>
        <RequestJoinWorkspaceModal visible={requestJoinWorkspaceVisible} setVisible={() => setRequestJoinWorkspaceVisible(false)}/>
        
        {/* Employee View of the Dashboard */}
        {user.role === "employee" && (
          <div className={styles.headerRow}>
            <h1 className={styles.title} data-testid="dashboard-h1">Dashboard</h1>
            {workspace == null && (<Button onClick={() => setRequestJoinWorkspaceVisible(true)} label="Request to join Workspace" />)}
          </div>
        )}

        {/* Admin View of the Dashboard */}
        {user.role === "admin" && (
          <div>
            <h1 data-testid="dashboard-h1">Dashboard</h1>
          </div>
        )}
        
        {/* This is how and where the notifications are loaded */}
        <Toast className={styles.d_toast} ref={toastNotifications} onRemove={(message) => handleRemove(message.id)} position="top-right" />
    </div>
  );
}

export default Dashboard;