import Invite from "../invites/invites";
import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { Toast } from "primereact/toast";
import { useOutletContext } from "react-router-dom";
import { useEffect, useState } from "react";
import { Button } from "primereact/button";
import RequestJoinWorkspaceModal from "../components/modals/RequestJoinWorkspaceModal.jsx";

function Dashboard({toast}) {

  const { toastNotifications, setNotifications, user, workspace } = useOutletContext();
  const [requestJoinWorkspaceVisible, setRequestJoinWorkspaceVisible] = useState(false);
  const [pendingUser, setPendingUser] = useState([])

  useEffect(() => {
    api.get("/auth/test")
    .then(res => {
      setPendingUser(res.data.pending)
    })
  }, [])

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
        <RequestJoinWorkspaceModal toast={toast} visible={requestJoinWorkspaceVisible} setVisible={() => setRequestJoinWorkspaceVisible(false)}/>
        
        {/* Employee View of the Dashboard */}
        {user?.role === "employee" && (
          <div className={styles.headerRow}>
            <h1 className={styles.title} data-testid="dashboard-h1">Dashboard</h1>
            {workspace == null && (<Button data-testid="request-join-workspace-button" onClick={() => setRequestJoinWorkspaceVisible(true)} disabled={pendingUser == null || pendingUser != true ? false : true} label={pendingUser == null || pendingUser != true ? "Request to Join Workspace" : "A request has been sent"} />)}
          </div>
        )}

        {/* Admin View of the Dashboard */}
        {user?.role === "admin" && (
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