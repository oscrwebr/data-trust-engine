import Invite from "../invites/invites";
import { Button } from "primereact/button";
import { useState, useRef } from "react";

function Dashboard({toast}) {
  const [visible, setVisible] = useState(false);

  return (
    <div>
        <h1>Dashboard</h1>
        <Button onClick={() => setVisible(true)}>Invite Employee</Button>
        <Invite visible={visible} setVisible={setVisible} toast={toast}/>
    </div>
  );
}

export default Dashboard;