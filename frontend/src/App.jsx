import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './Dashboard/Dashboard';
import EmployeeInviteError from './Invites/EmployeeInviteError';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/dashboard" element={<Dashboard/>}></Route>
        <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
      </Routes>
    </Router>
  );
}

export default App;