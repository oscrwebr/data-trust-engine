import { useRef, useEffect } from "react";
import { Button } from "primereact/button";
import { useLocation, useNavigate } from "react-router-dom";
import { Toast } from "primereact/toast";

function Home({toast}) {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const toastParam = params.get("toast");
  const shownRef = useRef(false);
  const successToast = useRef(null);
  const backend_uri = import.meta.env.VITE_BACKEND_HOST || "http://localhost:8000"
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

  useEffect(() => {
    if (!location.state) {return}
    if (location.state.status_code === 200) {
      successToast.current.show({
      severity: 'success',
      summary: 'Success',
      detail: 'You have logged out successfully!',
      life: 1000
    })} else {
      successToast.current.show({
      severity: 'error',
      summary: 'Error',
      detail: 'An error occurred while logging out.',
      life: 1000
    })}
    window.history.replaceState({}, '')
  }, [location.state])
  

  function handleCreateWorkspace(){
    console.log(backend_uri)
    window.location.href = `${backend_uri}/auth/sign-in?next=/create-workspace&signup=true&role=1`
  }

  function handleEmployeeSignup(){
    window.location.href = `${backend_uri}/auth/sign-in?next=/dashboard&signup=true&role=2`
  }

  function handleSignIn(){
    nav("/dashboard")
  }

  return (
    <div>
      <Toast ref={successToast}/>
      <Button onClick={handleSignIn}>Sign in</Button>
      <Button onClick={handleCreateWorkspace}>Create a workspace</Button>
      <Button onClick={handleEmployeeSignup}>Join a Workspace</Button>
    </div>
  );
}

export default Home;