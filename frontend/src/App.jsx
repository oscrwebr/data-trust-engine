import { useRef, useEffect } from "react";

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from './dashboard/Dashboard';
import EmployeeInviteError from './invites/error.jsx';
import Roles from "./roles/roles";
import CreateWorkspace from "./workspace/CreateWorkspace";
import { Button } from "primereact/button";
import { Toast } from 'primereact/toast';

import Test from "./Test/Test.jsx";
import Unprocessable422 from "./Errors/unprocessable422.jsx";
import Forbidden403 from "./Errors/Forbidden403.jsx";

function Home({toast}) {
  const params = new URLSearchParams(location.search);
  const toastParam = params.get("toast");
  const shownRef = useRef(false);

  useEffect(() => {
    if (toastParam && toast.current && !shownRef.current) {
      toast.current.show({ 
        severity: 'success', 
        summary: 'Success', 
        detail: 'You have joined your workspace!', 
        life: 4000 
      });
      shownRef.current = true;
    }
  }, [toastParam]);

  function handleCreateWorkspace(){
    window.location.href = "http://localhost:8000/auth/sign-in?next=/test&signup=true"
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
      <Routes>
        <Route path="/" element={<Home toast={toast}/>} />
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
