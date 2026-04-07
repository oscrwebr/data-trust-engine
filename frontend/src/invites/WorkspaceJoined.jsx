import { Link, useNavigate } from "react-router-dom";
import styles from "./invites.module.css";
import "primeicons/primeicons.css";

import logo from "../assets/CIH_logo.jpg";
import { Button } from "primereact/button";
import { Avatar } from "primereact/avatar";

function WorkspaceJoinedError(){
    const nav = useNavigate();
    
    function handleGoToWorkspace(){
        nav("/dashboard")
    }

    return (
        <div className={styles.e_container}>
            <div className={styles.e_error_container}>
                <h1 className={styles.e_error_title}>You've already joined a workspace <i style={{ fontSize: 25, marginLeft: 15  }} className="pi pi-check"></i></h1>
                <p className={styles.e_error_desc}>It looks like you’ve already joined this workspace. Click “Go to my workspace” to log in and access it. If this seems incorrect, contact your workspace administrator.</p>
                <Button className={styles.e_button} onClick={handleGoToWorkspace}>Go to my workspace</Button>
                <div className={styles.e_footer_container}>
                    <Link className={styles.e_home_link} to={`/`}>Return to home</Link>
                    <div className={styles.e_watermark_container}>
                        <Avatar image={logo} shape="circle" />
                        <p className={styles.e_dte_text}>The Data Trust Engine</p>
                    </div>
                </div>
            </div>
        </div> 
    )
}
  
export default WorkspaceJoinedError;
