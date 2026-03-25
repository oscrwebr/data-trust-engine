import { Outlet } from "react-router-dom";
import Header from "../header/header";
import Sidebar from "../navbar/Sidebar";
import { useState, useEffect, useRef } from "react";
import styles from "../layout/layout.module.css"
import api from "../../api/axiosConfig";

const Layout = () => {

  const toastNotifications = useRef(null);
  const [visible, setVisible] = useState(false);
  const [sidebarVisible, setSidebarVisible] = useState(true)
  const [user, setUser] = useState({});
  const [workspace, setWorkspace] = useState(null)
  const [notifications, setNotifications] = useState([])

// Getting user information and all their notifications on loading
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

  return (
    <div className={styles.container}>
        {sidebarVisible &&(<div className={styles.navbar_container}>
            <Sidebar setSidebarVisible={setSidebarVisible} firstname={user.firstname} surname={user.surname} email={user.email} setVisible={setVisible} role={user.role}/>
        </div>)}
        <div className={styles.main}>
            <Header firstname={user.firstname} lastname={user.surname} workspace={workspace} sidebarVisible={sidebarVisible} setSidebarVisible={setSidebarVisible} toastRef={toastNotifications} notifications={notifications} setNotifications={setNotifications}/>
            <div className={styles.content}>
                <Outlet context={{
                    toastNotifications,
                    visible,
                    setVisible,
                    setNotifications
                }} />
            </div>
        </div>
    </div>
  );
};

export default Layout;