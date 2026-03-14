import Invite from "../invites/invites";
import { Button } from "primereact/button";
import { useState, useEffect } from "react";
import api from "../api/axiosConfig.js";
import styles from "./dashboard.module.css"
import { Badge } from "primereact/badge"

function Dashboard({toast}) {
  const [visible, setVisible] = useState(false);
  const [user, setUser] = useState({});

  useEffect(() => {
      api.get("/workspace/dashboard")
      .then(res => {
          console.log(res)
          if (res.data.user) {
              setUser(res.data.user);
          }
      })
      .catch(error => console.log("This is the error from 'Test.jsx'" + error))
  }, []);

  return (
    <div>
        <div className={styles.header}>
          <h1>Dashboard</h1>
          <Button id={styles.bell_btn} text 
            style={{marginRight: 50, background: "transparent", border: "none", boxShadow: "none", outline: "none"}}
          ><i className="pi pi-bell p-overlay-badge" style={{ fontSize: 21}}><Badge value="2" severity="danger"></Badge></i></Button>
        </div>
        <Button onClick={() => setVisible(true)}>Invite Employee</Button>
        <Invite visible={visible} setVisible={setVisible} toast={toast}/>
    </div>
  );
}

export default Dashboard;