import { useRef } from "react";

import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from './dashboard/Dashboard';
import EmployeeInviteError from './invites/EmployeeInviteError';
import Roles from "./roles/roles";
import CreateWorkspace from "./Workspace/CreateWorkspace";
import { Toast } from 'primereact/toast';


function Home() {
  return (
    <div>
      <h1>Home Page</h1>
      <p>Welcome to the React + FastAPI app!</p>
    </div>
  );
}

function App() {
  const toast = useRef(null);

  return (
    <BrowserRouter>
      <Toast ref={toast} position="top-right"/>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/roles" element={<Roles />} />
        <Route path="/dashboard" element={<Dashboard toast={toast}/>} />
        <Route path="/create-workspace" element={<CreateWorkspace  toast={toast}/>} />
        <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
