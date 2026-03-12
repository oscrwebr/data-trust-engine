import Invite from "../invites/invites";
import { Button } from "primereact/button";
import { useState, useEffect } from "react";
import api from "../api/axiosConfig.js";

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
        <h1>Dashboard</h1>
        <Button onClick={() => setVisible(true)}>Invite Employee</Button>
        <Invite visible={visible} setVisible={setVisible} toast={toast}/>
    </div>
  );
}

export default Dashboard;