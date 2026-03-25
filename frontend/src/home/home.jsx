import { useRef, useEffect } from "react";
import { Button } from "primereact/button";
import { useLocation, useNavigate } from "react-router-dom";

function Home({toast}) {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const toastParam = params.get("toast");
  const shownRef = useRef(false);
  const nav = useNavigate();

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
    window.location.href = "http://localhost:8000/auth/sign-in?next=/create-workspace&signup=true&role=1"
  }

  function handleSignIn(){
    nav("/dashboard")
  }

  return (
    <div>
      <Button onClick={handleSignIn}>Sign in</Button>
      <Button onClick={handleCreateWorkspace}>Create a workspace</Button>
    </div>
  );
}

export default Home;