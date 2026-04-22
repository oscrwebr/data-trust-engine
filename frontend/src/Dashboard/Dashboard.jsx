import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { useOutletContext } from "react-router-dom";
import { useEffect, useState } from "react";
import { Button } from "primereact/button";
import RequestJoinWorkspaceModal from "../components/modals/RequestJoinWorkspaceModal.jsx";
import { Divider } from "primereact/divider";
import "../scans/scans.css"

function Dashboard({toast}) {

  const { user, workspace } = useOutletContext();
  const [requestJoinWorkspaceVisible, setRequestJoinWorkspaceVisible] = useState(false);
  const [pendingUser, setPendingUser] = useState([])
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get("/auth/test")
    .then(res => {
      setPendingUser(res.data.pending)
    });

    api.get("/dashboard/get_recent_activity")
    .then(response => {
      console.log(response.data)
      setRecentActivity(response.data);
      setLoading(false);
    })
    .catch(err => {
      setError(err);
      setLoading(false);
    })
  }, [])

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
            <div className="scan-header">
                <h1 className="detection-heading">
                    Dashboard
                </h1>
            <Divider/>
            </div>

          </div>
        )}
        
        {/* This is how and where the notifications are loaded */}
    </div>
  );
}

export default Dashboard;