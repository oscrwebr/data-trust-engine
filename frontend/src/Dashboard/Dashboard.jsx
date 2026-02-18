import "primereact/resources/themes/lara-light-indigo/theme.css"; 
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

import { useState } from "react";

import { Dialog } from "primereact/dialog";
import { Button } from "primereact/button";

function Dashboard() {
  const [visible, setVisible] = useState(false);

  return (
    <div>
      <Button onClick={() => setVisible(true)}>Invite Employee</Button>
      <Dialog visible={visible} onHide={() => setVisible(false)}/>
    </div>
  );
}

export default Dashboard;