import styles from "./employees.module.css"
import api from "../api/axiosConfig";

import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { useState, useEffect } from "react";
import { Dropdown } from 'primereact/dropdown';
import { Button } from "primereact/button";
import RowCard from "../components/employees/RowCard";
import SendMessage from "../components/employees/SendMessage";

function ViewEmployees(){
    const [selectedRole, setSelectedRole] = useState(null);
    const [selectedRisk, setSelectedRisk] = useState(null);
    const [searchValue, setSearchValue] = useState(null);
    const [employees, setEmployees] = useState([]);
    const [roles, setRoles] = useState([]);
    const [sendMessageDialog, setSendMessageDialog] = useState(false);
    const [view, setView] = useState(true);
    const [selectedEmployees, setSelectedEmployees] = useState([]);

    const onSelectedEmployeesChange = (id, checked) => {
        setSelectedEmployees(prev => {
            if (checked) {
                return [...prev, id];
            } else {
                return prev.filter(empId => empId !== id);
            }
        });
    };

    useEffect(() => {
        api.get("/workspace/get-employees")
        .then(res => {
            setEmployees(res.data)
        });

        api.get("/workspace/get-workspace-roles")
        .then(res => {
            const all = { id: "all", name: "View All Roles" };
            const none = { id: "null", name: "No Role Assigned" };
            setRoles([all, ...res.data, none]);
            
        });
    }, []);

    return(
        <div>
            <SendMessage visible={sendMessageDialog} setVisible={setSendMessageDialog} roles={roles} setRoles={setRoles}/>
            <div className={styles.container}>
                <h1 className={styles.title}>View Employees</h1>
                <Button disabled={selectedEmployees.length == 0 ? (true) : (false)} onClick={() => setSendMessageDialog(true)} className={styles.send_message_button}>Send a Message</Button>
            </div>
            <div className={styles.header}>
                <strong className={styles.employee_count}>{employees.length} People</strong>
                <div className={styles.search_dropdown_icon_container}>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown value={selectedRole} options={roles} onChange={(e) => setSelectedRole(e.value)} optionLabel="name" 
                            placeholder="Filter by Roles" className="p-inputtext-sm"/>
                    </div>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown value={selectedRisk} onChange={(e) => setSelectedRisk(e.value)} optionLabel="name" 
                            placeholder="Filter by Risk Level" className="p-inputtext-sm"/>
                    </div>
                    <IconField iconPosition="left">
                        <InputIcon className="pi pi-search"> </InputIcon>
                        <InputText onChange={(e) => setSearchValue(e.target.value)} style={{ width: '23vw'}} placeholder="Search by employee name or email" className="p-inputtext-sm"/>
                    </IconField>
                    <Button className={styles.view_button} onClick={() => setView(!view)}><i style={{ color:"black", fontSize:"20px" }} className={view ? "pi pi-list" : "pi pi-table"}/></Button>
                </div>
            </div>
            {view ? 

            // Employees displayed as rows
            (<div className={styles.row_container}>
                {employees
                    .filter(employee => {
                        const matchesRole =
                            !selectedRole ||
                            selectedRole.name === "View All Roles" ||
                            (selectedRole.name === "No Role Assigned" && employee.role_name === null) ||
                            employee.role_name === selectedRole.name;

                        const search = searchValue?.toLowerCase() || "";

                        const matchesSearch =
                            employee.user.firstname?.toLowerCase().includes(search) ||
                            employee.user.surname?.toLowerCase().includes(search) ||
                            employee.user.email?.toLowerCase().includes(search);

                        return matchesRole && matchesSearch;
                    })
                    .map((employee) => (
                        <RowCard
                            id={employee.user.user_id}
                            initials={
                                (employee.user.firstname?.[0]?.toUpperCase() || "?") +
                                (employee.user.surname?.[0]?.toUpperCase() || "?")
                            } 
                            firstname={employee.user.firstname}
                            surname={employee.user.surname}
                            email={employee.user.email}
                            role={employee.role_name || "No Role Assigned"}
                            onChange={onSelectedEmployeesChange}
                            checked={selectedEmployees.includes(employee.user.user_id)}
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