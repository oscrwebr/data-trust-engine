import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { useOutletContext } from "react-router-dom";
import { useEffect, useState } from "react";
import { Button } from "primereact/button";
import RequestJoinWorkspaceModal from "../components/modals/RequestJoinWorkspaceModal.jsx";
import { Divider } from "primereact/divider";
import "../scans/scans.css"
import { PiEnvelopeSimple } from "react-icons/pi";
import { PiUserGear } from "react-icons/pi";
import { PiClockClockwise } from "react-icons/pi";
import { PiCheckCircle } from "react-icons/pi";
import { useNavigate } from "react-router-dom";
import ReactTimeAgo from "react-time-ago"
import "react-time-ago/locale/en"




function Dashboard({toast}) {

  const { user, workspace } = useOutletContext();
  const [requestJoinWorkspaceVisible, setRequestJoinWorkspaceVisible] = useState(false);
  const [pendingUser, setPendingUser] = useState([])
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const [dashboardSummary, setDashboardSummary] = useState(null); 

  useEffect(() => {
    api.get("/auth/test")
    .then(res => {
      setPendingUser(res.data.pending)
    });

    api.get("/dashboard/get_recent_activity")
    .then(response => {
      
      setRecentActivity(response.data);
      setLoading(false);
    })
    .catch(err => {
      setError(err);
      setLoading(false);
    })

    api.get("/dashboard/get_dashboard_summary")
    .then(response => {
      setDashboardSummary(response.data);
    })
  }, [])

  function formatText(activity){
    switch(activity.type) {
      case "scan_started":
        return `${activity.scan_type.charAt(0).toUpperCase() + activity.scan_type.slice(1)} Scan Started`;
      case "scan_completed":
        return `${activity.scan_type.charAt(0).toUpperCase() + activity.scan_type.slice(1)} Scan Completed`;
      case "invite":
        return "Employee Invitation Sent";
      case "role_change":
        return "Workspace Role Updated";
      default:
        return "Unknown Activity";
    }
  }

  const activityIcons = {
    "scan_started": <PiClockClockwise size={22} />,
    "scan_completed": <PiCheckCircle size={22} />,
    "invite": <PiEnvelopeSimple size={22} />,
    "role_change": <PiUserGear size={22} />
  }

  function handleActivityClick(activity) {
    switch(activity.type) {
      case "scan_started":
      case "scan_completed":
        navigate(`/scans/${activity.scan_id}`);
        break;
      case "invite":
        navigate("/manage-employees")
      case "role_change":
        navigate("/roles")
    }
  }

  return (
    <div className={styles.container}>
        <RequestJoinWorkspaceModal toast={toast} visible={requestJoinWorkspaceVisible} setVisible={() => setRequestJoinWorkspaceVisible(false)}/>
        
        {/* Employee View of the Dashboard */}
        {user?.role === "employee" && (
          <div className={styles.header_container}>
            <div className={styles.header_container_2}>
                <i id={styles.icon} className="pi pi-compass"/>
                <h1 className={styles.title} data-testid="dashboard-h1">Dashboard</h1>
            </div>
            {workspace == null && (<Button data-testid="request-join-workspace-button" onClick={() => setRequestJoinWorkspaceVisible(true)} disabled={pendingUser == null || pendingUser != true ? false : true} label={pendingUser == null || pendingUser != true ? "Request to Join Workspace" : "A request has been sent"} />)}
          </div>
        )}

        {/* Admin View of the Dashboard */}
        {user?.role === "admin" && (
        <div>
          <div className="scan-header">
                  <div className={styles.headerRow}>
                    <i id={styles.icon} className="pi pi-compass"/>
                    <h1 className={styles.title} data-testid="dashboard-h1">Dashboard</h1>
                  </div>
                  <Divider/>
              </div>

              <div>
                <h2 className={styles.welcomeHeading}>Welcome back, {user.firstname}!</h2>
              </div>

              <div className={styles.summaryContainer}>
                {/* Total employees card */}
                <div className={styles.summaryCard}>
                  <span className={styles.summaryCardLabel}>Total Employees</span>
                  <span className={styles.summaryCardValue}>
                    {dashboardSummary?.total_employees ?? 0}
                  </span>
                </div>

                {/* Total pending users card */}
                <div className={styles.summaryCard}>
                  <span className={styles.summaryCardLabel}>Pending Users</span>
                  <span className={styles.summaryCardValue}>
                    {dashboardSummary?.pending_users ?? 0}
                  </span>
                </div>

                {/* Total workspace files card */}
                <div className={styles.summaryCard}>
                  <span className={styles.summaryCardLabel}>Workspace Files</span>
                  <span className={styles.summaryCardValue}>
                    {dashboardSummary?.total_files ?? 0}
                  </span>
                </div>
              </div>

              <div className={styles.recentActivityCard}>
                <h2 className={styles.recentActivityHeader}>Recent Activity</h2>
                 {loading ? (
                    <p>Loading recent activity...</p>
                  ) : error ? (
                    <p>Error loading recent activity.</p>
                  ) : recentActivity.length === 0 ? (
                    <p>No recent activity found.</p>
                  ) : (
                    <div className={styles.activityList}>
                      {recentActivity.map((activity, index) => (
                        <div key={index} className={styles.activityItem} onClick={() => handleActivityClick(activity)}>
                          <div className={styles.activityIconBox}>
                            {activityIcons[activity.type]}
                          </div>
                          <div className={styles.activityContent}>
                            <span className={styles.activityText}>{formatText(activity)}</span>
                            <span className={styles.activityTime}><ReactTimeAgo date={new Date(activity.timestamp)} locale="en-US" /></span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
              </div>

        </div>
        )}
    </div>
  );
}

export default Dashboard;