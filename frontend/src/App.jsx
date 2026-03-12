import "./App.css"
import { useRef } from "react";

import { BrowserRouter, Routes, Route , useLocation} from "react-router-dom";
import Dashboard from './dashboard/Dashboard';
import EmployeeInviteError from './invites/error.jsx';
import Roles from "./roles/roles";
import CreateWorkspace from "./workspace/CreateWorkspace";
import Home from "./home/home.jsx"
import { Toast } from 'primereact/toast';
import Scans from "./scans/Scans.jsx";

import Test from "./Test/Test.jsx";
import Navbar from "./components/navbar/Navbar.jsx";
import Unprocessable422 from "./Errors/unprocessable422.jsx";
import Forbidden403 from "./Errors/Forbidden403.jsx";

function App() {
  const toast = useRef(null);

  // Not making navbar visible on 'home' page
  // Ref: https://www.reddit.com/r/reactjs/comments/kvoj5d/comment/gtfmh2s/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
  const location = useLocation();

  return (
    <>
    <Toast ref={toast} position="top-right"/>

    
      
    {location.pathname !== "/" && <Navbar />}
    <div className={location.pathname !== "/" ? "content-frame" : ""}>
      <Routes>
        <Route path="/" element={<Home toast={toast}/>} />
        <Route path="/roles" element={<Roles />} />
        <Route path="/dashboard" element={<Dashboard toast={toast}/>} />
        <Route path="/create-workspace" element={<CreateWorkspace  toast={toast}/>} />
        <Route path="/test" element={<Test/>} />
        <Route path="/error/422" element={<Unprocessable422/>}/>
        <Route path="/error/403" element={<Forbidden403/>}/>
        <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
        <Route path="/scans" element={<Scans />} />
      </Routes>
    </div>
    </>
  );
}

export default App;
