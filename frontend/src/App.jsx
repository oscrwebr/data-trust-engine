import "./App.css"
import { useRef } from "react";

import { BrowserRouter, Routes, Router, Route , useLocation} from "react-router-dom";
import Dashboard from './Dashboard/Dashboard';
import EmployeeInviteError from './invites/error.jsx';
import Roles from "./roles/roles";
import CreateWorkspace from "./workspace/CreateWorkspace";
import Home from "./home/home.jsx"
import FileOverviewPage from "./FileOverview/FileOverviewPage.jsx";
import HighRiskFilesDashboard from "./HighRiskFilesDashboard/HighRiskFilesDashboard.jsx";
import { Toast } from 'primereact/toast';
import Scans from "./scans/Scans.jsx";
import FilesDashboard from "./FilesDashboard/filesDashboard.jsx";
import AdminFiles from "./AdminFiles/adminFiles.jsx"
import Test from "./Test/Test.jsx";
import Unprocessable422 from "./Errors/Unprocessable422.jsx";
import WorkspaceJoinedError from "./invites/WorkspaceJoined.jsx";
import Forbidden403 from "./Errors/Forbidden403.jsx";
import Layout from "./components/layout/layout.jsx";
import OrgChart from "./org_chart/orgChart";
import ViewEmployees from "./employees/ViewEmployees.jsx";
import ManageEmployees from "./employees/ManageEmployees.jsx";
import ScanPage from "./scans/ScanPage.jsx";
import OrganisationalDevTest from "./scan_dev_test/OrganisationalDevTest.jsx";
import ScanFile from "./scan_file/ScanFile.jsx";



function App() {
  const toast = useRef(null);

  // Not making navbar visible on 'home' page
  // Ref: https://www.reddit.com/r/reactjs/comments/kvoj5d/comment/gtfmh2s/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
  const location = useLocation();

  return (
    <>
    <Toast ref={toast} position="top-right"/>
      <Routes>
        <Route element={<Layout />}>

          {/* Elements in here will inherit the sidebar  */}
          <Route path="/roles" element={<Roles />} />
          <Route path="/view-employees" element={<ViewEmployees toast={toast}/>} />
          <Route path="/manage-employees" element={<ManageEmployees toast={toast}/>} />
          <Route path="/upload-org-chart" element={<OrgChart toast={toast} />} />
          <Route path="/settings" element={null} />
          <Route path="/dashboard" element={<Dashboard toast={toast}/>} />
          <Route path="/my-files" element={<FilesDashboard toast={toast}/>} />
          <Route path="/workspace-files" element={<AdminFiles toast={toast}/>} />
          <Route path="/files/:file_id" element={<FileOverviewPage toast={toast}/>} />
          <Route path="/scans" element={<Scans />} />
          <Route path="/scans/:scanId" element={<ScanPage/>} />
          <Route path="/org-scan-dev" element={<OrganisationalDevTest />} />
          <Route path="/high-risk-files" element={<HighRiskFilesDashboard />} />
          <Route path="scan-file/:scanFileId" element={<ScanFile/>} />
        </Route>

        {/* Elements in here will not inherit the sidebar */}
        <Route path="/" element={<Home toast={toast}/>} />
        <Route path="/dashboard" element={<Dashboard toast={toast}/>} />
        <Route path="/create-workspace" element={<CreateWorkspace  toast={toast}/>} />
        <Route path="/test" element={<Test/>} />
        <Route path="/error/422" element={<Unprocessable422/>}/>
        <Route path="/error/403" element={<Forbidden403/>}/>
        <Route path="/invite-error/:type" element={<EmployeeInviteError toast={toast}/>} />
        <Route path="/workspace-joined" element={<WorkspaceJoinedError />} />        
      </Routes>

    </>
  );
}

export default App;
