import "./App.css"
import { useRef } from "react";

import { BrowserRouter, Routes, Route, useNavigate} from "react-router-dom";
import Dashboard from './dashboard/Dashboard';
import EmployeeInviteError from './invites/error.jsx';
import Roles from "./roles/roles";
import CreateWorkspace from "./Workspace/CreateWorkspace";
import { Button } from "primereact/button";
import { Toast } from 'primereact/toast';

import axios from 'axios';
import Test from "./Test/Test.jsx";
import Navbar from "./components/navbar/Navbar.jsx";
import Unprocessable422 from "./Errors/unprocessable422.jsx";
import Forbidden403 from "./Errors/Forbidden403.jsx";

function Home() {
  const navigate = useNavigate();

  function handleCreateWorkspace(){
    navigate("/create-workspace")
  }

  return (
    <div>
      <Button onClick={handleCreateWorkspace}>Create a workspace</Button>
    </div>
  );
}

function App() {
  const toast = useRef(null);

  return (
    <BrowserRouter>
      <Toast ref={toast} position="top-right"/>
    <Navbar/>
    <div className="content-frame">
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
    </div>
    </BrowserRouter>
  );
}

export default App;
