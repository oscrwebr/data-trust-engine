import { Outlet } from "react-router-dom";
import Header from "../header/header";
import Sidebar from "../navbar/Sidebar";
import { useState, useEffect, useRef } from "react";
import styles from "../layout/layout.module.css"
import api from "../../api/axiosConfig";
import { Toast } from "primereact/toast";

const Layout = () => {

  const toastNotifications = useRef(null);
  const [visible, setVisible] = useState(false);
  const [sidebarVisible, setSidebarVisible] = useState(true)
  const [user, setUser] = useState({});
  const [workspace, setWorkspace] = useState(null)
  const [notifications, setNotifications] = useState([])
  const [pendingEmployees, setPendingEmployees] = useState([])

// Getting user information and all their notifications on loading
  useEffect(() => {
      api.get("/workspace/dashboard")
      .then(res => {
          if (res.data.user) {
            setUser(res.data.user);
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

  const fetchPendingEmployees = () => {
    api.get("/workspace/get-pending-employees")
      .then(res => setPendingEmployees(res.data))
      .catch(err => console.log(err));
  };

  useEffect(() => {
    fetchPendingEmployees();
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
        {sidebarVisible &&(<div className={styles.navbar_container}>
            <Sidebar setSidebarVisible={setSidebarVisible} firstname={user.firstname} surname={user.surname} email={user.email} setVisible={setVisible} role={user.role} pendingEmployees={pendingEmployees}/>
        </div>)}
        <div className={styles.main}>
            <Header firstname={user.firstname} lastname={user.surname} workspace={workspace} sidebarVisible={sidebarVisible} setSidebarVisible={setSidebarVisible} toastRef={toastNotifications} notifications={notifications} setNotifications={setNotifications}/>
            <div className={styles.content}>
                <Outlet context={{
                    visible,
                    setVisible,
                    user,
                    workspace,
                    pendingEmployees,
                    setPendingEmployees,
                    fetchPendingEmployees
                }} />
            </div>
            <Toast className={styles.d_toast} ref={toastNotifications} onRemove={(message) => handleRemove(message.id)} position="top-right" />
        </div>
    </div>
  );
};

export default Layout;