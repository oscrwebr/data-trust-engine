import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
import styles from "./roles.module.css";

function Roles() {
  const [roles, setRoles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [users, setUsers] = useState([]); // For User Assignment
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [activePanel, setActivePanel] = useState("roles"); // "roles" or "users"

  // Form state for Add / Edit Role
  const [editingRole, setEditingRole] = useState(null);
  const [roleName, setRoleName] = useState("");
  const [thresholds, setThresholds] = useState({});

  // ----------------- Filter & Search -----------------
  const [roleFilter, setRoleFilter] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  // Filtered users
  const filteredUsers = users.filter((user) => {
    const matchesSearch =
      `${user.firstname} ${user.surname}`.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRole = !roleFilter || user.role_id === parseInt(roleFilter);
    return matchesSearch && matchesRole;
  });

  // -------------------------
  // Fetch roles, categories, subcategories, and users
  // -------------------------
  useEffect(() => {
    async function fetchData() {
      try {
        const [rolesRes, categoriesRes, subsRes, usersRes] = await Promise.all([
          api.get("/roles/get"),
          api.get("/roles/sensitivity/categories"),
          api.get("/roles/sensitivity/subcategories"),
          api.get("/roles/users/all")  // fetch all users once
        ]);
  
        setRoles(rolesRes.data);
        setUsers(usersRes.data);
  
        const groupedCategories = categoriesRes.data.map((cat) => ({
          ...cat,
          subcategories: subsRes.data.filter(
            (sub) => sub.sensitivity_category_id === cat.sensitivity_category_id
          ),
        }));
  
        setCategories(groupedCategories);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch roles, categories, or users");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // -------------------------
  // Role Handlers
  // -------------------------
  const mapThresholdsForAPI = () =>
    Object.entries(thresholds)
      .filter(([_, value]) => value !== null && value !== "")
      .map(([subId, value]) => ({
        sensitivity_subcategory_id: parseInt(subId, 10),
        threshold: parseInt(value, 10),
      }));

  const handleEditClick = (role) => {
    setEditingRole(role);
    setRoleName(role.name);

    const initialThresholds = {};
    role.role_permissions?.forEach((perm) => {
      initialThresholds[perm.sensitivity_subcategory_id] = perm.threshold;
    });
    setThresholds(initialThresholds);
  };

  const handleCancelEdit = () => {
    setEditingRole(null);
    setRoleName("");
    setThresholds({});
  };

  const handleDeleteRole = async () => {
    if (!editingRole) return;
    try {
      await api.delete(`/roles/delete/${editingRole.role_id}`);
      setRoles(roles.filter((r) => r.role_id !== editingRole.role_id));
      handleCancelEdit();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveRole = async () => {
    if (!roleName.trim()) return;
    const payload = {
      name: roleName,
      thresholds: mapThresholdsForAPI()
    };

    try {
      if (editingRole) {
        await api.put(`/roles/update/${editingRole.role_id}`, payload);
        const rolesRes = await api.get("/roles/get");
        setRoles(rolesRes.data);
        handleCancelEdit();
      } else {
        const res = await api.post("/roles/create", payload);
        setRoles([...roles, res.data]);
        setRoleName("");
        setThresholds({});
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleThresholdChange = (subId, value) => {
    setThresholds({
      ...thresholds,
      [subId]: value === "" ? null : parseInt(value, 10),
    });
  };

  // -------------------------
  // User Assignment Handler
  // -------------------------
  const handleUserRoleChange = async (userId, newRoleId) => {
    try {
      await api.put(`/roles/users/${userId}/role`, { role_id: newRoleId });
  
      // Update frontend state
      const roleName = roles.find((r) => r.role_id === parseInt(newRoleId))?.name || "";
  
      setUsers(users.map((u) =>
        u.user_id === userId
          ? { ...u, role_id: parseInt(newRoleId), role_name: roleName }
          : u
      ));
    } catch (err) {
      console.error(err);
    }
  };
  if (loading) return <p className={styles.message}>Loading...</p>;
  if (error) return <p className={styles.error}>{error}</p>;

  return (
    <div className={styles.pageContainer}>
      {/* ---------------- Buttons ---------------- */}
      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
        <button
          onClick={() => setActivePanel("roles")}
          className={activePanel === "roles" ? styles.activeTab : ""}
        >
          Roles Management
        </button>
        <button
          onClick={() => setActivePanel("users")}
          className={activePanel === "users" ? styles.activeTab : ""}
        >
          User Assignment
        </button>
      </div>

      {/* ---------------- Panel ---------------- */}
      {activePanel === "roles" ? (
        <main className={styles.main}>
          {/* Left panel: existing roles */}
          <div className={styles.leftPanel}>
            <h2>Existing Roles</h2>
            <ul className={styles.roleList}>
              {roles.map((role) => (
                <li key={role.role_id} className={styles.roleItem}>
                  <span>{role.name}</span>
                  <button
                    onClick={() => handleEditClick(role)}
                    className={styles.editButton}
                  >
                    Edit
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Right panel: Add / Edit Role */}
          <div className={styles.rightPanel}>
            <h2>{editingRole ? "Edit Role" : "Add New Role"}</h2>

            <input
              type="text"
              placeholder="Role Name"
              value={roleName}
              onChange={(e) => setRoleName(e.target.value)}
              className={styles.input}
            />

            <h3>Set Sensitivity Thresholds</h3>
            {categories.map((cat) => (
              <div key={cat.sensitivity_category_id}>
                <div className={styles.sensitivityCategory}>{cat.name}</div>
                {cat.subcategories.map((sub) => (
                  <div
                    key={sub.sensitivity_subcategory_id}
                    className={styles.subRow}
                  >
                    <label>{sub.name}</label>
                    <input
                      type="number"
                      min="1"
                      placeholder="Null"
                      value={thresholds[sub.sensitivity_subcategory_id] ?? ""}
                      onChange={(e) =>
                        handleThresholdChange(
                          sub.sensitivity_subcategory_id,
                          e.target.value
                        )
                      }
                      className={styles.input}
                    />
                  </div>
                ))}
              </div>
            ))}

            <div
              style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}
            >
              <button onClick={handleSaveRole} className={styles.addButton}>
                {editingRole ? "Save Changes" : "Add Role"}
              </button>
              {editingRole && (
                <>
                  <button
                    onClick={handleCancelEdit}
                    className={styles.cancelButton}
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleDeleteRole}
                    className={styles.deleteButton}
                  >
                    Delete
                  </button>
                </>
              )}
            </div>
          </div>
        </main>
      ) : (
        <main className={styles.main}>
          <div className={styles.rightPanel} style={{ width: "100%" }}>
            <h2>User Assignment</h2>

            {/* Filter + Search */}
            <div className={styles.filterBar}>
              <input
                type="text"
                placeholder="Search by username..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className={styles.searchInput}
              />
              <select
                value={roleFilter}
                onChange={(e) => setRoleFilter(e.target.value)}
                className={styles.roleFilter}
              >
                <option value="">All Roles</option>
                {roles.map((role) => (
                  <option key={role.role_id} value={role.role_id}>
                    {role.name}
                  </option>
                ))}
              </select>
            </div>

            {/* User List */}
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {filteredUsers.map((user) => (
                <div key={user.user_id} className={styles.userRow}>
                  <span title={`${user.firstname} ${user.surname}`}>
                    {user.firstname} {user.surname}
                  </span>
                  <select
                    value={user.role_id || ""}
                    onChange={(e) => handleUserRoleChange(user.user_id, e.target.value)}
                  >
                    {roles.map((role) => (
                      <option key={role.role_id} value={role.role_id}>
                        {role.name}  {/* now shows PII / Financial / Legal */}
                      </option>
                    ))}
                  </select>                
                </div>
              ))}
            </div>
          </div>
        </main>
      )}
    </div>
  );
}

export default Roles;