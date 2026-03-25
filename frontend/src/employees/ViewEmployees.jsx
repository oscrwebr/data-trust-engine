import styles from "./employees.module.css"
import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import React, { useState } from "react";
import { Dropdown } from 'primereact/dropdown';
import { Button } from "primereact/button";

function ViewEmployees(){
    const [selectedRole, setSelectedRole] = useState([]);
    const [view, setView] = useState(false)

    return(
        <div>
            <h1 className={styles.title}>View Employees</h1>
            <div className={styles.header}>
                <strong>Employee Count:</strong>
                <div className={styles.search_dropdown_icon_container}>
                    <IconField iconPosition="left" style={{ marginRight:"20px" }}>
                        <InputIcon className="pi pi-search"> </InputIcon>
                        <InputText style={{ width: '23vw'}} placeholder="Search by employee name or email" className="p-inputtext-sm"/>
                    </IconField>
                    <div className="card flex justify-content-center">
                        <Dropdown value={selectedRole} onChange={(e) => setSelectedRole(e.value)} optionLabel="name" 
                            placeholder="Filter by Departments" className="p-inputtext-sm"/>
                    </div>
                    <Button className={styles.view_button} onClick={() => setView(!view)}><i style={{ color:"black", fontSize:"20px" }} className={view ? "pi pi-list" : "pi pi-table"}/></Button>
                </div>
            </div>
        </div>
    )
}

export default ViewEmployees;