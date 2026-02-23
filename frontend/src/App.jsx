import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from './Dashboard/Dashboard';
import Roles from "./roles/roles";

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
      </Routes>
    </BrowserRouter>
  );
}

export default App;
