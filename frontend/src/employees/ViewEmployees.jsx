import styles from "./employees.module.css"
import api from "../api/axiosConfig";

import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { useState, useEffect } from "react";
import { Dropdown } from 'primereact/dropdown';
import { Button } from "primereact/button";
import RowCard from "./RowCard";

function ViewEmployees(){
    const [selectedRole, setSelectedRole] = useState([]);
    const [employees, setEmployees] = useState([])
    const [view, setView] = useState(false)

     useEffect(() => {
        api.get("/workspace/get-employees")
        .then(res => {
            setEmployees(res.data)
        });
    }, []);

    return(
        <div>
            <h1 className={styles.title}>View Employees</h1>
            <div className={styles.header}>
                <strong>Employee Count: {employees.length}</strong>
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
            {view ? 

            // Employees displayed as rows
            (<div>
                {employees.map((employee) => (
                    <RowCard 
                        initials={(employee.firstname?.[0]?.toUpperCase() || "?") + (employee.surname?.[0]?.toUpperCase() || "?")} 
                        firstname={employee.firstname}
                        surname={employee.surname}
                        email={employee.email}
                        role={employee.role}
                    />
                ))}
            </div>

            ) : (
            
            // Employees displayed as squares
            <div>

            </div>
            )}
        </div>
    )
}

export default ViewEmployees;