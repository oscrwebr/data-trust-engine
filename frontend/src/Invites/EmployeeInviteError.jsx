import { Link, useParams, useSearchParams } from "react-router-dom";
import dayjs from "dayjs";
import styles from "./EmployeeInvite.module.css";
import "primeicons/primeicons.css";

import logo from "../assets/CIH_logo.jpg";
import { Button } from "primereact/button";
import {Avatar} from "primereact/Avatar";
import { useEffect, useState } from "react";

function EmployeeInviteError(){

    const [searchParams] = useSearchParams();
    const expiry = searchParams.get("date");      
    let params = useParams();
    const [error_desc, setErrorDesc] = useState("")

    useEffect(() => {
            if(params.type == "expired"){ 
                setErrorDesc(<>The invite that your supervisor sent you expired on the <strong>{dayjs(expiry).format("D MMMM YYYY")}</strong>. To access your workspace, please ask your supervisor to send a new invite link</>)
            } else {
                setErrorDesc(<>This invite that your supervisor sent you has already been used. To access your workspace, please ask your supervisor to send a new invite link.</>);
            }
    }, []);

    return (
        <div className={styles.e_container}>
            <div className={styles.e_error_container}>
                <h1 className={styles.e_error_title}>This invite link is no longer valid <i style={{ marginLeft: 15, fontSize: 25 }} className="pi pi-clock"></i></h1>
                <p className={styles.e_error_desc}>{error_desc}</p>
                <Button className={styles.e_button}>Request to join workspace</Button>
                <div className={styles.e_footer_container}>
                    <Link className={styles.e_home_link} to={`/dashboard`}>Return to home</Link>
                    <div className={styles.e_watermark_container}>
                        <Avatar image={logo} shape="circle" />
                        <p className={styles.e_dte_text}>The Data Trust Engine</p>
                    </div>
                </div>
            </div>
        </div> 
    )
}
  
export default EmployeeInviteError
