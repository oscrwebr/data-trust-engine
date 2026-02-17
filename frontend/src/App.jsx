import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then(res => res.json())
      .then(data => setStatus(data.status));
  }, []);

  return (
    <div>
      <h1>React + FastAPI</h1>
      <p>Backend status: {status}</p>
    </div>
  );
}

export default App;