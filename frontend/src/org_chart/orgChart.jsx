import React, { useState } from "react";
import api from "../api/axiosConfig.js";
import { useNavigate } from "react-router-dom";

import { FileUpload } from "primereact/fileupload";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import styles from "./orgChart.module.css";

function OrgChart({ toast }) {
  const navigate = useNavigate();

  const [file, setFile] = useState([]);
  const [fileError, setFileError] = useState(false);
  const [previewData, setPreviewData] = useState(null);
  const [loading, setLoading] = useState(false);

  const [showAddUser, setShowAddUser] = useState(false);
  const [newUser, setNewUser] = useState({ name: "", email: "", role: null });

  const showSuccess = (message) => {
    toast.current.show({
      severity: "success",
      summary: "Success",
      detail: message,
      life: 4000,
    });
  };

  const onFileSelect = (e) => {
    setFile(e.files);
    setFileError(false);
  };

  const handleParseFile = async () => {
    if (!file || file.length === 0) {
      setFileError(true);
      return;
    }
    setFileError(false);
    setLoading(true);

    const formData = new FormData();
    formData.append("orgChart", file[0]);

    try {
      const response = await api.post("/org-chart/parse-orgchart", formData);
      setPreviewData(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const sourceRoleIndex = previewData.roles.findIndex(
      (role) => role.name === result.source.droppableId
    );
    const destRoleIndex = previewData.roles.findIndex(
      (role) => role.name === result.destination.droppableId
    );

    const sourceEmployees = Array.from(previewData.roles[sourceRoleIndex].employees);
    const [movedEmployee] = sourceEmployees.splice(result.source.index, 1);

    if (sourceRoleIndex === destRoleIndex) {
      sourceEmployees.splice(result.destination.index, 0, movedEmployee);
      const newRoles = [...previewData.roles];
      newRoles[sourceRoleIndex].employees = sourceEmployees;
      setPreviewData({ ...previewData, roles: newRoles });
    } else {
      const destEmployees = Array.from(previewData.roles[destRoleIndex].employees);
      destEmployees.splice(result.destination.index, 0, movedEmployee);

      const newRoles = [...previewData.roles];
      newRoles[sourceRoleIndex].employees = sourceEmployees;
      newRoles[destRoleIndex].employees = destEmployees;
      setPreviewData({ ...previewData, roles: newRoles });
    }
  };

  const handleDeleteEmployee = (roleIndex, empIndex) => {
    const newRoles = [...previewData.roles];
    newRoles[roleIndex].employees.splice(empIndex, 1);
    setPreviewData({ ...previewData, roles: newRoles });
  };

  const handleAddUser = () => {
    if (!newUser.name || !newUser.email || !newUser.role) return;

    const roleIndex = previewData.roles.findIndex((r) => r.name === newUser.role);
    const newRoles = [...previewData.roles];
    newRoles[roleIndex].employees.push({ name: newUser.name, email: newUser.email });
    setPreviewData({ ...previewData, roles: newRoles });

    setShowAddUser(false);
    setNewUser({ name: "", email: "", role: null });
    showSuccess("User added successfully!");
  };

  const handleAccept = async () => {
    if (!previewData) return;

    try {
      await api.post("/org-chart/confirm-orgchart", { roles: previewData.roles });
      showSuccess("Org chart saved successfully!");
      navigate("/dashboard");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className={styles.orgPageContainer}>
      <h2 className={styles.pageHeader}>Organisation Chart</h2>

      {/* Upload Section */}
      {!previewData && (
        <div className={styles.orgUploadSection}>
          <label className={styles.orgLabel}>Upload Org Chart (Excel / CSV)</label>

          <FileUpload
            name="orgChart"
            customUpload
            uploadHandler={onFileSelect}
            accept=".xlsx,.xls,.csv"
            maxFileSize={5 * 1024 * 1024}
            chooseLabel="Click or Drag File Here"
            mode="basic"
            multiple={false}
            className={styles.fileUpload}
          />

          {fileError && <div className={styles.message + " " + styles.error}>You must upload an organisation chart.</div>}

          {file.length > 0 && (
            <div className={styles.selectedFile}>
              <strong>Selected File:</strong> {file[0].name}
            </div>
          )}

          <button onClick={handleParseFile} className={`${styles.btn} ${styles.parseBtn}`} disabled={loading}>
            {loading ? "Parsing..." : "Parse Org Chart"}
          </button>
        </div>
      )}

      {/* Preview Section */}
      {previewData && (
        <div className={styles.orgPreviewSection}>
          <h3 className={styles.orgPreviewTitle}>Organisation Structure</h3>

          <button
            className={`${styles.btn} ${styles.addBtn}`}
            onClick={() => setShowAddUser(!showAddUser)}
            style={{ marginBottom: "15px" }}
          >
            {showAddUser ? "Cancel Add User" : "Add User"}
          </button>

          {/* Add User Form */}
          {showAddUser && (
            <div className={styles.orgAddUserForm}>
              <label>Name</label>
              <input
                type="text"
                value={newUser.name}
                onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                className={styles.inputField}
              />

              <label>Email</label>
              <input
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                className={styles.inputField}
              />

              <label>Role</label>
              <select
                value={newUser.role}
                onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                className={styles.roleDropdown}
              >
                <option value="">Select Role</option>
                {previewData.roles.map((r) => (
                  <option key={r.name} value={r.name}>{r.name}</option>
                ))}
              </select>

              <button className={`${styles.btn} ${styles.addBtn}`} onClick={handleAddUser}>Add User</button>
            </div>
          )}

          {/* Drag & Drop Org Chart */}
          <DragDropContext onDragEnd={handleDragEnd}>
            {previewData.roles.map((role, roleIndex) => (
              <Droppable key={role.name} droppableId={role.name}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className={styles.roleBlock}
                  >
                    <h4 className={styles.roleTitle}>{role.name}</h4>

                    {role.employees.map((emp, empIndex) => (
                      <Draggable
                        key={`${role.name}-${emp.email}`}
                        draggableId={`${role.name}-${emp.email}`}
                        index={empIndex}
                      >
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={styles.userRow}
                          >
                            <span className={styles.userName}>{emp.name} ({emp.email})</span>
                            <button
                              className={`${styles.btn} ${styles.deleteBtn}`}
                              onClick={() => handleDeleteEmployee(roleIndex, empIndex)}
                            >
                              ×
                            </button>
                          </div>
                        )}
                      </Draggable>
                    ))}

                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            ))}
          </DragDropContext>

          <div className={styles.orgActionButtons}>
            <button className={`${styles.btn} ${styles.cancelBtn}`} onClick={() => setPreviewData(null)}>Back</button>
            <button className={`${styles.btn} ${styles.saveBtn}`} onClick={handleAccept}>Accept & Save Org Chart</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default OrgChart;