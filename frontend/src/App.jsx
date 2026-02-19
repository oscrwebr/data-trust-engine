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
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/roles" element={<Roles />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
