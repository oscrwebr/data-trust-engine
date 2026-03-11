import { useRef, useEffect } from "react";
import { Button } from "primereact/button";

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

export default Home;