import styles from "./employees.module.css"
import api from "../api/axiosConfig"
import { useEffect } from "react";

import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { useState } from "react";
import { Dropdown } from 'primereact/dropdown';
import { Button } from "primereact/button";

function ManageEmployees({toast}){
    const [selectedRole, setSelectedRole] = useState(null);
    const [selectedStatus, setSelectedStatus] = useState(null);
    const [searchValue, setSearchValue] = useState(null);
    const [view, setView] = useState(true);
    const [employees, setEmployees] = useState([])
    const [roles, setRoles] = useState([])
    const [pendingEmployees, setPendingEmployees] = useState([])

    useEffect(() => {
        api.get("/workspace/get-employees")
        .then(res => {
            setEmployees(res.data.active);
            setPendingEmployees(res.data.pending);
        });

        api.get("/workspace/get-workspace-roles")
        .then(res => {
            const all = { id: "all", name: "View All Roles" };
            const none = { id: "null", name: "No Role Assigned" };
            setRoles([all, ...res.data, none]);
        });
    }, []);

    return(
        <div className={styles.page}>
            <div>
                <h1 className={styles.title}>Manage Employees</h1>
            </div>
            <div className={styles.header}>
                <div className={styles.count_container}>
                    <strong className={styles.active_employee_count}>{employees.length} Active Employees</strong>
                    <strong className={styles.pending_employee_count}>{pendingEmployees.length} Pending Employees</strong>
                </div>
                <div className={styles.search_dropdown_icon_container}>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown data-testid="roles-dropdown" value={selectedRole} onChange={(e) => setSelectedRole(e.value)} optionLabel="name" 
                            placeholder="Filter by Roles" className="p-inputtext-sm"/>
                    </div>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown value={selectedStatus} onChange={(e) => setSelectedStatus(e.value)} optionLabel="name" 
                            placeholder="Filter by Status" className="p-inputtext-sm"/>
                    </div>
                    <IconField iconPosition="left">
                        <InputIcon className="pi pi-search"></InputIcon>
                        <InputText onChange={(e) => setSearchValue(e.target.value)} style={{ width: '23vw'}} placeholder="Search by employee name or email" className="p-inputtext-sm"/>
                    </IconField>
                    <Button data-testid="display-change-button" className={styles.view_button} onClick={() => setView(!view)}><i style={{ color:"black", fontSize:"20px" }} className={view ? "pi pi-list" : "pi pi-table"}/></Button>
                </div>
            </div>
        </div>
    )
}

export default ManageEmployees;