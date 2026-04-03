import { Link, useParams, useSearchParams } from "react-router-dom";
import dayjs from "dayjs";
import styles from "./invites.module.css";
import "primeicons/primeicons.css";
import api from "../api/axiosConfig"

import logo from "../assets/CIH_logo.jpg";
import { Button } from "primereact/button";
import {Avatar} from "primereact/Avatar";
import { useEffect, useState } from "react";

function EmployeeInviteError({toast}){

    const [searchParams] = useSearchParams();
    const expiry = searchParams.get("date");  
    const workspace_id = searchParams.get("workspace");      
    const [isDisabled, setIsDisabled] = useState(false);
    const title = "New Invite Request"
    const body = "An employee has requested join your workspace. You can review this request in Manage Employees."

    useEffect(() => {
        const storedState = localStorage.getItem('buttonDisabled');
        if (storedState === 'true') {
            setIsDisabled(true); 
        }
    }, []);

    const showRequestSentSuccess = () => {
      toast.current.show({ severity: 'success', summary: 'Success', detail: 'Invite request sent!', life: 4000});
    };

    const handleRequestJoinWorkspace = async () => {
        setIsDisabled(true);
        localStorage.setItem('buttonDisabled', 'true'); 
        try {
            await api.post("/workspace/request-join-workspace", {
                title: title,
                body: body,
                workspace_id: workspace_id,
            }).then(res => {
                showRequestSentSuccess();
            })
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className={styles.e_container}>
            <div className={styles.e_error_container}>
                <h1 className={styles.e_error_title}>This invite link is no longer valid <i style={{ marginLeft: 15, fontSize: 25 }} className="pi pi-clock"></i></h1>
                <p className={styles.e_error_desc}>The invite that your supervisor sent you expired on the <strong>{dayjs(expiry).format("D MMMM YYYY")}</strong>. To access your workspace, please ask your supervisor to send a new invite link</p>
                <Button onClick={handleRequestJoinWorkspace} className={styles.e_button} disabled={isDisabled}>Request to join workspace</Button>
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
  
export default EmployeeInviteError;
