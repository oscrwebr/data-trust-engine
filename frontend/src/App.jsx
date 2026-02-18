import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Roles from "./components/roles/roles";

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
      <div>
        <nav style={{ marginBottom: "1rem" }}>
          <Link to="/" style={{ marginRight: "1rem" }}>Home</Link>
          <Link to="/roles">Roles</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/roles" element={<Roles />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
