import { useRef, useEffect } from "react";
import { Button } from "primereact/button";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./home.module.css";

function Home({toast}) {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const toastParam = params.get("toast");
  const shownRef = useRef(false);
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
    if (location.state?.status_code === 200) {
      toast?.current.show({
      severity: 'success',
      summary: 'Success',
      detail: 'You have logged out successfully!',
      life: 1000
    })} else {
      toast?.current.show({
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
    <div className={styles.body}>
      <div className={styles.container}>
        <div className={styles.hero}>
          <span className={styles.primary_title}>The Data Trust Engine</span>
          <span className={styles.secondary_title}>Building Trust in Every Data Interaction</span>
          <span className={styles.tertiary_title}>Enable secure collaboration and controlled access between organizations. Create <br/>
            trusted data environments where teams can work together with confidence.</span>
          <div className={styles.chip_container}>
            <div className={styles.chip}>
              <i className="pi pi-check-circle"/>
              <span>Secure</span>      
            </div>
            <i className="pi pi-circle-fill"/>
            <div className={styles.chip}>
              <i className="pi pi-check-circle"/>
              <span>Scalable</span>         
            </div>
            <i className="pi pi-circle-fill"/>
            <div className={styles.chip}>
              <i className="pi pi-check-circle"/>
              <span>Compliant</span>
            </div>
          </div>
          <div>
            <Button className={styles.create_a_workspace} onClick={handleCreateWorkspace}><i className="pi pi-shield"/> Create a Workspace</Button>
            <Button className={styles.get_started} onClick={handleEmployeeSignup}><i className="pi pi-user-plus"/> Get Started</Button>
          </div>
          <Button className={styles.sign_in} onClick={handleSignIn}><i className="pi pi-sign-in"/> Sign in</Button>
        </div>
        <div className={styles.line}/>
        <span className={styles.how_it_works}>How it Works</span>
        <div className={styles.feature_card_container}>
          
        </div>
      </div>
    </div>
  );
}

export default Home;