import { useRef } from "react";

import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from './dashboard/Dashboard';
import EmployeeInviteError from './invites/EmployeeInviteError';
import Roles from "./roles/roles";
import CreateWorkspace from "./Workspace/CreateWorkspace";
import { Toast } from 'primereact/toast';

import Test from "./Test/Test.jsx";
import Unprocessable422 from "./Errors/unprocessable422.jsx";
import Forbidden403 from "./Errors/Forbidden403.jsx";

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
        <Route path="/test" element={<Test/>} />
        <Route path="/error/422" element={<Unprocessable422/>}/>
        <Route path="/error/403" element={<Forbidden403/>}/>
        <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
