import { Link } from "react-router-dom";
import styles from "./EmployeeInvite.module.css";
import "primeicons/primeicons.css";

import logo from "../assets/CIH_logo.jpg";
import { Button } from "primereact/button";
import {Avatar} from "primereact/Avatar";

function EmployeeInviteError({description}){
    return (
        <div className={styles.d_error_container}>
            <h1 className={styles.d_error_title}>This invite link is no longer valid <i style={{ marginLeft: 10 }} className="pi pi-clock"></i></h1>
            <p className={styles.d_error_desc}>{description}</p>
            <Button className={styles.d_button}>Request to join workspace</Button>
            <Link className={styles.d_home_link} to={`/dashboard`}>Return to home</Link>
            <div className={styles.d_swatermark_container}>
                <Avatar image={logo} shape="circle" />
                <p>The Data Trust Engine</p>
            </div>
        </div>
    )
}
  
export default EmployeeInviteError
