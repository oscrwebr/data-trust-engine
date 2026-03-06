import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from './dashboard/Dashboard';
import EmployeeInviteError from './invites/EmployeeInviteError';
import Roles from "./roles/roles";
import CreateWorkspace from "./Workspace/CreateWorkspace";

function Home() {
  return (
    <div>
      <h1>Home Page</h1>
      <p>Welcome to the React + FastAPI app!</p>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/roles" element={<Roles />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/create-workspace" element={<CreateWorkspace />} />
        <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
