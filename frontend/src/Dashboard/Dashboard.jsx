import EmployeeInvite from "../Invites/EmployeeInvite";
import { Button } from "primereact/button";
import { useState } from "react";

function Dashboard() {
  const [visible, setVisible] = useState(false);

  return (
    <div>
        <h1>Dashboard</h1>
        <Button onClick={() => setVisible(true)}>Invite Employee</Button>
        <EmployeeInvite visible={visible} setVisible={setVisible} />
    </div>
  );
}

export default Dashboard;