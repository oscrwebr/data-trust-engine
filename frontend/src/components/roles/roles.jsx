import { useEffect, useState } from "react";
import api from "../../api/axiosConfig";
import styles from "./styles.module.css";

function Roles() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newRoleName, setNewRoleName] = useState("");
  const [editingRoleId, setEditingRoleId] = useState(null);
  const [editingRoleName, setEditingRoleName] = useState("");

  useEffect(() => {
    async function fetchRoles() {
      try {
        const response = await api.get("/roles/get");
        setRoles(response.data);
      } catch (err) {
        console.error("Error fetching roles:", err);
        setError("Failed to fetch roles");
      } finally {
        setLoading(false);
      }
    }
    fetchRoles();
  }, []);

  const handleAddRole = async () => {
    if (!newRoleName.trim()) return;
    try {
      const response = await api.post("/roles/create", { name: newRoleName });
      setRoles([...roles, response.data]);
      setNewRoleName("");
    } catch (err) {
      console.error("Error adding role:", err);
    }
  };

  const handleDeleteRole = async (id) => {
    try {
      await api.delete(`/roles/delete/${id}`);
      setRoles(roles.filter((role) => role.id !== id));
    } catch (err) {
      console.error("Error deleting role:", err);
    }
  };

  const handleEditClick = (role) => {
    setEditingRoleId(role.id);
    setEditingRoleName(role.name);
  };

  const handleEditSave = async (roleId) => {
    if (!editingRoleName.trim()) return;
    try {
      const response = await api.put(`/roles/update/${roleId}`, { name: editingRoleName });
      setRoles(roles.map((r) => (r.id === roleId ? response.data : r)));
      setEditingRoleId(null);
      setEditingRoleName("");
    } catch (err) {
      console.error("Error updating role:", err);
    }
  };

  return (
    <div className={styles.pageContainer}>
      <header className={styles.header}>
        <h1 className={styles.title}>Roles Management</h1>
        <p className={styles.subtitle}>
          Manage user roles and permissions across your organization
        </p>
      </header>

      <main className={styles.main}>
        <div className={styles.addRole}>
          <input
            type="text"
            placeholder="New role name..."
            value={newRoleName}
            onChange={(e) => setNewRoleName(e.target.value)}
            className={styles.input}
            onKeyDown={(e) => e.key === "Enter" && handleAddRole()}
          />
          <button onClick={handleAddRole} className={styles.addButton}>
            Add
          </button>
        </div>

        {loading ? (
          <p className={styles.message}>Loading roles...</p>
        ) : error ? (
          <p className={styles.error}>{error}</p>
        ) : roles.length === 0 ? (
          <p className={styles.message}>No roles found.</p>
        ) : (
          <ul className={styles.roleList}>
            {roles.map((role) => (
              <li key={role.id} className={styles.roleItem}>
                {editingRoleId === role.id ? (
                  <>
                    <input
                      value={editingRoleName}
                      onChange={(e) => setEditingRoleName(e.target.value)}
                      className={styles.inputEdit}
                      onKeyDown={(e) => e.key === "Enter" && handleEditSave(role.id)}
                      autoFocus
                    />
                    <button
                      onClick={() => handleEditSave(role.id)}
                      className={styles.saveButton}
                    >
                      Save
                    </button>
                  </>
                ) : (
                  <>
                    <span
                      onClick={() => handleEditClick(role)}
                      className={styles.roleName}
                    >
                      {role.name}
                    </span>
                    <button
                      onClick={() => handleDeleteRole(role.id)}
                      className={styles.deleteButton}
                    >
                      ✕
                    </button>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}

export default Roles;
