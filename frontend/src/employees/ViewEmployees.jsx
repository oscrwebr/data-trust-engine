import styles from "./employees.module.css"
import api from "../api/axiosConfig";

import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { useState, useEffect } from "react";
import { Dropdown } from 'primereact/dropdown';
import { Button } from "primereact/button";
import { Checkbox } from "primereact/checkbox";
import RowCard from "../components/view_employees/RowCard";
import SendMessage from "../components/view_employees/SendMessage";
import SquareCard from "../components/view_employees/SquareCard";
import Invite from "../invites/invites";

function ViewEmployees({toast}){
    const [selectedRole, setSelectedRole] = useState(null);
    const [selectedRisk, setSelectedRisk] = useState(null);
    const [searchValue, setSearchValue] = useState(null);
    const [employees, setEmployees] = useState([]);
    const [roles, setRoles] = useState([]);
    const [sendMessageDialog, setSendMessageDialog] = useState(false);
    const [view, setView] = useState(true);
    const [selectedEmployees, setSelectedEmployees] = useState([]);
    const [sendInviteModal, setSendInviteModal] = useState(false)

    const onSelectedEmployeesChange = (employee, checked) => {
        setSelectedEmployees(prev => {
            if (checked) {
                return [...prev, employee];
            } else {
                return prev.filter(emp => emp.user.user_id !== employee.user.user_id);
            }
        });
    };

    const onRemove = (id) => {
        setSelectedEmployees(prev => 
            prev.filter(emp => emp.user.user_id !== id)
        );
    }

    useEffect(() => {
        api.get("/workspace/get-employees")
        .then(res => {
            setEmployees(res.data.active)
            console.log(res.data.active)
        });

        api.get("/workspace/get-workspace-roles")
        .then(res => {
            const all = { id: "all", name: "View All Roles" };
            const none = { id: "null", name: "No Role Assigned" };
            setRoles([all, ...res.data, none]);
        });
    }, []);

    const filteredEmployees = employees.filter(employee => {
        const matchesRole =
            !selectedRole ||
            selectedRole.name === "View All Roles" ||
            (selectedRole.name === "No Role Assigned" && employee.role_name === null) ||
            employee.role_name === selectedRole.name;

        const matchesRisk =
            !selectedRisk ||
            selectedRisk === "View All Scanning Risks" ||
            employee.files.status === selectedRisk;

        const search = searchValue?.toLowerCase() || "";

        const matchesSearch =
            employee.user.firstname?.toLowerCase().includes(search) ||
            employee.user.surname?.toLowerCase().includes(search) ||
            employee.user.email?.toLowerCase().includes(search);

        return matchesRole && matchesSearch && matchesRisk;
    });

    const riskOptions = ["View All Scanning Risks", "No Risk Detected", "Risk Detected", "No Files Found", "No Files Scanned"]

    return(
        <div className={styles.page}>
            <SendMessage visible={sendMessageDialog} setVisible={setSendMessageDialog} selectedEmployees={selectedEmployees} setSelectedEmployees={setSelectedEmployees} onRemove={onRemove} toast={toast}/>
            <Invite className={styles.d_invite_dialog} visible={sendInviteModal} setVisible={setSendInviteModal} toast={toast}/>
            <div className={styles.container}>
                <h1 className={styles.title}>View Employees</h1>
                <div>
                    <Button data-testid="send-invite" style={{ marginRight: '10px'}} onClick={() => setSendInviteModal(true)} >Send an Invite</Button>
                    <Button data-testid="send-message-button" disabled={selectedEmployees.length == 0 ? (true) : (false)} onClick={() => setSendMessageDialog(true)}>Send a Message</Button>
                </div>
            </div>
            <div className={styles.header}>
                <strong className={styles.employee_count}>{employees.length} People</strong>
                <div className={styles.search_dropdown_icon_container}>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown data-testid="roles-dropdown" value={selectedRole} options={roles} onChange={(e) => setSelectedRole(e.value)} optionLabel="name" 
                            placeholder="Filter by Roles" className="p-inputtext-sm"/>
                    </div>
                    <div className="card flex justify-content-center" style={{ marginRight:"15px" }}>
                        <Dropdown value={selectedRisk} options={riskOptions} onChange={(e) => setSelectedRisk(e.value)} optionLabel="name" 
                            placeholder="Filter by Risk Level" className="p-inputtext-sm"/>
                    </div>
                    <IconField iconPosition="left">
                        <InputIcon className="pi pi-search"></InputIcon>
                        <InputText onChange={(e) => setSearchValue(e.target.value)} style={{ width: '23vw'}} placeholder="Search by employee name or email" className="p-inputtext-sm"/>
                    </IconField>
                    <div className={styles.select_all_container}>
                        <span>Select All</span>
                        <div className="card flex justify-content-center">
                            <Checkbox data-testid="select-all-checkbox" style={{ marginLeft: '10px' }}

                                checked={selectedEmployees.length === filteredEmployees.length && filteredEmployees.length > 0}
                                onChange={(e) => {
                                    const checked = e.checked;
                                    setSelectedEmployees(checked ? [...filteredEmployees] : []);
                                }}/>
                        </div>
                    </div>
                    <Button data-testid="display-change-button" className={styles.view_button} onClick={() => setView(!view)}><i style={{ color:"black", fontSize:"20px" }} className={view ? "pi pi-list" : "pi pi-table"}/></Button>
                </div>
            </div>
            <div className={styles.list_container}>
                {view ? (
                    // Row Cards
                    filteredEmployees.map(employee => (
                        <div className={styles.row_container} key={employee.user.user_id}>
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
                                risk={employee.files}
                                onChange={(id, checked) => onSelectedEmployeesChange(employee, checked)}
                                checked={selectedEmployees.some(emp => emp.user.user_id === employee.user.user_id)}
                            />
                        </div>
                    ))
                ) : (
                    // Square Cards
                    <div className={styles.square_container}>
                        {filteredEmployees.map(employee => (
                            <SquareCard
                                key={employee.user.user_id}
                                id={employee.user.user_id}
                                initials={
                                    (employee.user.firstname?.[0]?.toUpperCase() || "?") +
                                    (employee.user.surname?.[0]?.toUpperCase() || "?")
                                }
                                firstname={employee.user.firstname}
                                surname={employee.user.surname}
                                email={employee.user.email}
                                role={employee.role_name || "No Role Assigned"}
                                risk={employee.files}
                                onChange={(id, checked) => onSelectedEmployeesChange(employee, checked)}
                                checked={selectedEmployees.some(emp => emp.user.user_id === employee.user.user_id)}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}

export default ViewEmployees;