import styles from "./employees.module.css"
import api from "../api/axiosConfig"
import { useEffect } from "react";

import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { useState } from "react";
import { Dropdown } from 'primereact/dropdown';
import { Button } from "primereact/button";

import ActiveEmployeeRow from "../components/manage_employees/ActiveEmployeeRow";
import ActiveEmployeeSquare from "../components/manage_employees/ActiveEmployeeSquare";
import PendingEmployeeRow from "../components/manage_employees/PendingEmployeeRow";
import PendingEmployeeSquare from "../components/manage_employees/PendingEmployeeSquare";

function ManageEmployees({toast}){
    const [employeeRoles, setEmployeeRoles] = useState({});
    const [selectedRole, setSelectedRole] = useState(null)
    const [selectedStatus, setSelectedStatus] = useState(null);
    const [searchValue, setSearchValue] = useState(null);
    const [view, setView] = useState(true);
    const [employees, setEmployees] = useState([])
    const [roles, setRoles] = useState([])
    const [status, _] = useState(["View All Employees", "Active", "Pending"])
    const [pendingEmployees, setPendingEmployees] = useState([])
     const [mixedUsers, setMixedUsers] = useState([]);

    useEffect(() => {
        api.get("/workspace/get-employees")
        .then(res => {
            setEmployees(res.data.active);
            setPendingEmployees(res.data.pending);
        });

        api.get("/workspace/get-workspace-roles")
        .then(res => {
            const all = { id: "all", name: "View All Employees" };
            const none = { id: "null", name: "No Role Assigned" };
            setRoles([all, ...res.data, none]);
        });
    }, []);

    useEffect(() => {
        const combined = [
            ...pendingEmployees.map(u => ({ ...u, status: "Pending" })),
            ...employees.map(u => ({ ...u, status: "Active" }))
        ];

        for (let i = combined.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [combined[i], combined[j]] = [combined[j], combined[i]];
        }

        setMixedUsers(combined);
    }, [pendingEmployees, employees]);

    const filteredEmployees = mixedUsers.filter(employee => {
        const matchesRole =
            !selectedRole ||
                selectedRole.name === "View All Employees" ||
                (selectedRole.name === "No Role Assigned" && employee.role_name === null) ||
                employee.role_name === selectedRole.name

        const matchesStatus =
            !selectedStatus ||
                selectedStatus === "View All Employees" ||
                employee.status === selectedStatus

        const search = searchValue?.toLowerCase() || "";

        const matchesSearch = employee.status === "Active"
            ? (
                (employee.user?.firstname?.toLowerCase().includes(search) || false) ||
                (employee.user?.surname?.toLowerCase().includes(search) || false) ||
                (employee.user?.email?.toLowerCase().includes(search) || false)
            )
            : (
                employee.pending?.email?.toLowerCase().includes(search) || false
            );

        return matchesRole && matchesStatus && matchesSearch;
    });

    const handleRoleChange = (employee_id, new_role, original_role) => {
        setEmployeeRoles(prev => {
            if (new_role === original_role) {
                const updated = { ...prev };
                delete updated[employee_id];
                return updated;
            }

            return {
                ...prev,
                [employee_id]: new_role
            };
        });
    };

    const handleRemoveEmployee = (employee_id) => {
        api.delete(`/workspace/delete-user/${employee_id}`)
        .then(res => {
            showSuccessMessageRemove();
        })

        api.get("/workspace/get-employees")
        .then(res => {
            setEmployees(res.data.active);
            setPendingEmployees(res.data.pending);
        });
    }

    const showSuccessMessageRemove = () => {
        toast.current.show({ severity: 'success', summary: 'Success', detail: 'Employee succesfully removed!', life: 4000});
    };

    return(
        <div className={styles.page}>
            <div className={styles.container}>
                <h1 className={styles.title}>Manage Employees</h1>
                <Button data-testid="save-information" disabled={Object.keys(employeeRoles).length === 0}>Save Information</Button>
            </div>
            <div className={styles.header}>
                <div className={styles.count_container}>
                    <strong className={styles.active_employee_count}>{employees.length} Active Employees</strong>
                    <strong className={styles.pending_employee_count}>{pendingEmployees.length} Pending Employees</strong>
                </div>
                <div className={styles.search_dropdown_icon_container}>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown data-testid="roles-dropdown" options={roles} value={selectedRole} onChange={(e) => setSelectedRole(e.value)} optionLabel="name" 
                            placeholder="Filter by Roles" className="p-inputtext-sm"/>
                    </div>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown value={selectedStatus} options={status} onChange={(e) => setSelectedStatus(e.value)} optionLabel="name" 
                            placeholder="Filter by Status" className="p-inputtext-sm"/>
                    </div>
                    <IconField iconPosition="left">
                        <InputIcon className="pi pi-search"></InputIcon>
                        <InputText onChange={(e) => setSearchValue(e.target.value)} style={{ width: '23vw'}} placeholder="Search by employee name or email" className="p-inputtext-sm"/>
                    </IconField>
                    <Button data-testid="display-change-button" className={styles.view_button} onClick={() => setView(!view)}><i style={{ color:"black", fontSize:"20px" }} className={view ? "pi pi-list" : "pi pi-table"}/></Button>
                </div>
            </div>
            <div className={styles.list_container}>
                {/* Mapping the mixed users to their cards */}
                {view ? (
                    filteredEmployees.map((employee, index) => (
                    <div className={styles.row_container} key={index}>

                        {/* Row view for active users*/}
                        {employee.status === "Active" && (                  
                            <ActiveEmployeeRow initials={
                                (employee.user.firstname?.[0]?.toUpperCase() || "?") +
                                (employee.user.surname?.[0]?.toUpperCase() || "?")
                            } 
                                id={employee.user.user_id}
                                firstname={employee.user.firstname}
                                surname={employee.user.surname}
                                email={employee.user.email}
                                employeeRole={(employeeRoles[employee.user.user_id] ?? employee.role_name) || "No Role Assigned"}
                                roles={roles}
                                setEmployeeRole={(role) => handleRoleChange(employee.user.user_id, role, employee.role_name || "No Role Assigned")}
                                removeEmployee={() => handleRemoveEmployee(employee.user.user_id)}/>
                        )}

                        {employee.status === "Pending" && (
                            <PendingEmployeeRow 
                                email={employee.pending.email} status={employee.pending.type} datetime={employee.datetime}/>
                        )}
                    </div>
                    ))
                ) : (
                    <div className={styles.square_container}>
                        {filteredEmployees.map((employee, index) => {

                            if (employee.status === "Active") {
                                return (
                                    <ActiveEmployeeSquare initials={
                                        (employee.user.firstname?.[0]?.toUpperCase() || "?") +
                                        (employee.user.surname?.[0]?.toUpperCase() || "?")
                                    } firstname={employee.user.firstname} surname={employee.user.surname} email={employee.user.email} employeeRole={employee.role_name || "No Role Assigned"} roles={roles} setEmployeeRole={setSelectedRole} onRemove={() => handleRemoveEmployee(employee.user.user_id)}/>
                                )
                            }
                                
                            
                            if(employee.status === "Pending") {
                                return (
                                    <PendingEmployeeSquare
                                    email={employee.pending.email} status={employee.pending.type} datetime={employee.datetime}/>
                                )
                            }
                        })}
                    </div>
                )}
            </div>
        </div>
    )
}

export default ManageEmployees;