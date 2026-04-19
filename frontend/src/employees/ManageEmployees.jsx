    import styles from "./employees.module.css"
    import api from "../api/axiosConfig"
    import { useEffect } from "react";

    import { IconField } from "primereact/iconfield";
    import { InputIcon } from "primereact/inputicon";
    import { InputText } from "primereact/inputtext";
    import { useState } from "react";
    import { Dropdown } from 'primereact/dropdown';
    import { Button } from "primereact/button";

    import ActiveEmployeeRow from "../components/manage_employees/active_employee_cards/ActiveEmployeeRow";
    import ActiveEmployeeSquare from "../components/manage_employees/active_employee_cards/ActiveEmployeeSquare";
    import PendingEmployeeRow from "../components/manage_employees/pending_employee_cards/PendingEmployeeRow";
    import PendingEmployeeSquare from "../components/manage_employees/pending_employee_cards/PendingEmployeeSquare";
    import EmployeeRemoveModal from "../components/manage_employees/validation_modals/EmployeeRemoveModal";
    import PendingRejectModal from "../components/manage_employees/validation_modals/PendingRejectModal";
    import PendingAcceptModal from "../components/manage_employees/validation_modals/PendingAcceptModal";
    import Invite from "../invites/invites";
import { useOutletContext } from "react-router-dom";

    function ManageEmployees({toast}){
        const [employeeRoles, setEmployeeRoles] = useState({});
        const [selectedRole, setSelectedRole] = useState(null)
        const [selectedStatus, setSelectedStatus] = useState(null);
        const [searchValue, setSearchValue] = useState(null);
        const [view, setView] = useState(true);
        const [employees, setEmployees] = useState([])
        const [roles, setRoles] = useState([])
        const [status, _] = useState(["View All Employees", "Active", "Pending"])
        const [mixedUsers, setMixedUsers] = useState([]);
        const [user, setUser] = useState(null)
        const [removeEmployeeModal, setRemoveEmployeeModal] = useState(false)
        const [rejectPendingModal, setRejectPendingModal] = useState(false)
        const [acceptPendingModal, setAcceptPendingModal] = useState(false)
        const [saving, setSaving] = useState(false);
        const [sendInviteModal, setSendInviteModal] = useState(false)
        const [allPendingUsers, setAllPendingUsers] = useState([])
        const { pendingEmployees, setPendingEmployees } = useOutletContext();

        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 7);
        expiryDate.setMilliseconds(0);

        const fetchEmployees = () => {
            return api.get("/workspace/get-employees")
                .then(res => {
                    const active = (res.data.active || []).map(u => ({ ...u, status: "Active" }));
                    const pending = (res.data.pending || []).map(u => ({ ...u, status: "Pending" }));
                    const combined = [...active, ...pending];
                    
                    for (let i = combined.length - 1; i > 0; i--) {
                        const j = Math.floor(Math.random() * (i + 1));
                        [combined[i], combined[j]] = [combined[j], combined[i]];
                    }

                    setEmployees(active);
                    setAllPendingUsers(pending);
                    setMixedUsers(combined);
                }
            );
        };

        useEffect(() => {
            fetchEmployees();
            api.get("/workspace/get-workspace-roles")
                .then(res => {
                    const all = { id: "all", name: "View All Employees" };
                    const none = { id: "null", name: "No Role Assigned" };
                    setRoles([all, ...res.data, none]);
                });
        }, []);

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

        const handleSaveInformation = () => {
            if (Object.keys(employeeRoles).length === 0) return;
            setSaving(true);
            const payload = Object.entries(employeeRoles).map(([user_id, role_name]) => ({
                user_id: parseInt(user_id), 
                role_name
            }));

            api.put(`/roles/update-user-roles`, {
                employees: payload

            }).then(res => {
                showSuccessMessageUpdate();
                fetchEmployees();
                setEmployeeRoles({});
            })
            .catch(err => console.error("Error updating roles:", err))
            .finally(() => setSaving(false));
        }

        const handleRemoveEmployee = () => {
            api.delete(`/workspace/delete-user/${user.user_id}`)
                .then(res => {
                    showSuccessMessageRemove();
                    fetchEmployees();
                })
                .catch(err => console.error(err));
        }

        const handleRejectPending = () => {
            api.patch(`/workspace/reject-pending/${user.user_id}`)
                .then(res => {
                    showSuccessMessageReject();
                    fetchEmployees();
                })
                .catch(err => console.error(err));
        }

        const handleAcceptPending = async () => {
            await api.post(`/invite/send-invite`, {
                email: user.email || null,
                expiry_date: expiryDate ? expiryDate.toISOString() : null,
            })
            .then(res => {
                if(res.data.success == "invalid"){
                    showErrorMessageInvalid();
                } else if (res.data.success == "trust") {
                    showErrorMessageTrust();
                } else if (res.data.success == "cooldown") {
                    showErrorMessageCooldown();
                } else {
                    showSuccessMessageAccept();
                    fetchEmployees();
                }
                
            })
        }

        const showSuccessMessageRemove = () => {
            toast.current.show({ severity: 'info', summary: 'Info', detail: 'The employee was removed from your workspace.', life: 4000});
        };

        const showSuccessMessageAccept= () => {
            toast.current.show({ severity: 'info', summary: 'Info', detail: 'An invite has been sent to the employee.', life: 4000});
        };

        const showSuccessMessageReject = () => {
            toast.current.show({ severity: 'info', summary: 'Info', detail: 'The employee was rejected from your workspace.', life: 4000});
        };

        const showSuccessMessageUpdate = () => {
            toast.current.show({ severity: 'info', summary: 'Info', detail: 'The information was updated.', life: 4000});
        };

        const showErrorMessageTrust = () => {
            toast.current.show({ severity: 'error', summary: 'Error', detail: 'The email you are trying to send an invite to is untrustworthy.', life: 4000});
        };

        const showErrorMessageCooldown = () => {
            toast.current.show({ severity: 'error', summary: 'Error', detail: 'You are sending this employee too many invites, please try again tomorrow.', life: 4000});
        };

        const showErrorMessageInvalid = () => {
            toast.current.show({ severity: 'error', summary: 'Error', detail: 'The email you are trying to send an invite to does not exist.', life: 4000});
        };

        return(
            <div className={styles.page}>
                <EmployeeRemoveModal firstname={user?.firstname || ""} surname={user?.surname || ""} visible={removeEmployeeModal} setVisible={() => setRemoveEmployeeModal(false)} onRemove={() => {setRemoveEmployeeModal(false); handleRemoveEmployee();}}/>
                <PendingRejectModal email={user?.email || ""} visible={rejectPendingModal} setVisible={() => setRejectPendingModal(false)} onReject={() => {setRejectPendingModal(false); handleRejectPending();}}/>
                <PendingAcceptModal email={user?.email || ""} visible={acceptPendingModal} setVisible={() => setAcceptPendingModal(false)} onAccept={() => {setAcceptPendingModal(false); handleAcceptPending();}} date={expiryDate}/>
                <Invite className={styles.d_invite_dialog} visible={sendInviteModal} setVisible={setSendInviteModal} toast={toast}/>
                <div className={styles.container}>
                    <h1 className={styles.title}>Manage Employees</h1>
                    <div>
                        <Button data-testid="send-invite" style={{ marginRight: '10px'}} onClick={() => setSendInviteModal(true)} >Send an Invite</Button>
                        <Button data-testid="save-information" onClick={() => handleSaveInformation()} disabled={Object.keys(employeeRoles).length === 0 || saving}>Save Information</Button>
                    </div>
                </div>
                <div className={styles.header}>
                    <div className={styles.count_container}>
                        <strong className={styles.active_employee_count}>{employees.length} Active Employees</strong>
                        <strong className={styles.pending_employee_count}>{allPendingUsers.length} Pending Employees</strong>
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
                                    removeEmployee={() => {
                                        setRemoveEmployeeModal(true);
                                        setUser(employee.user);
                                    }}/>
                            )}

                            {employee.status === "Pending" && (
                                <PendingEmployeeRow 
                                    email={employee.pending.email} status={employee.pending.type} datetime={employee.datetime} onReject={() => {setRejectPendingModal(true); setUser(employee.pending);}} onAccept={() => {setAcceptPendingModal(true); setUser(employee.pending);}}/>
                            )}
                        </div>
                        ))
                    ) : (
                        <div className={styles.square_container}>
                            {filteredEmployees.map((employee, index) => {

                                if (employee.status === "Active") {
                                    return (
                                        <ActiveEmployeeSquare id={employee.user.user_id} initials={
                                            (employee.user.firstname?.[0]?.toUpperCase() || "?") +
                                            (employee.user.surname?.[0]?.toUpperCase() || "?")
                                        } firstname={employee.user.firstname} surname={employee.user.surname} email={employee.user.email} employeeRole={(employeeRoles[employee.user.user_id] ?? employee.role_name) || "No Role Assigned"} roles={roles} setEmployeeRole={(role) => handleRoleChange(employee.user.user_id, role, employee.role_name || "No Role Assigned")}
                                            removeEmployee={() => {
                                                setRemoveEmployeeModal(true);
                                                setUser(employee.user);
                                            }}
                                        />  
                                    )
                                }
                                    
                                
                                if(employee.status === "Pending") {
                                    return (
                                        <PendingEmployeeSquare
                                        email={employee.pending.email} status={employee.pending.type} datetime={employee.datetime} onReject={() => {setRejectPendingModal(true); setUser(employee.pending);}} onAccept={() => {setAcceptPendingModal(true); setUser(employee.pending);}}/>
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