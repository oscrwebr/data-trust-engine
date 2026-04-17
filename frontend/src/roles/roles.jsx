import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
import styles from "./roles.module.css";
import { RiUserSettingsLine } from "react-icons/ri";
import RoleCard from "./RoleCard";

import { Button } from "primereact/button";
import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { Dropdown } from "primereact/dropdown";
import EditRoleSidebar from "./EditRoleSidebar";

function Roles() {
  const [roles, setRoles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchValue, setSearchValue] = useState(null);
  const [editSidebar, setEditSidebar] = useState(false);

  // Form state for Add / Edit Role
  const [editingRole, setEditingRole] = useState(null);
  const [roleName, setRoleName] = useState("");
  const [thresholds, setThresholds] = useState({});

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
    console.log("clicked")
    setEditingRole(role);
    setRoleName(role.name);

    const initialThresholds = {};
    role.role_permissions?.forEach((perm) => {
      initialThresholds[perm.sensitivity_subcategory_id] = perm.threshold;
    });
    setThresholds(initialThresholds);
    setEditSidebar(true)
  };

  const handleCancelEdit = () => {
    setEditingRole(null);
    setRoleName("");
    setThresholds({});
    setEditSidebar(false);
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
        setEditSidebar(false);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // -------------------------
  // User Assignment Handler
  // -------------------------

  if (loading) return <p className={styles.message}>Loading...</p>;
  if (error) return <p className={styles.error}>{error}</p>;

  return (
    <div className={styles.pageContainer}>
      <EditRoleSidebar 
          role={editingRole} 
          visible={editSidebar} 
          setVisible={setEditSidebar} 
          categories={categories} 
          setThresholds={setThresholds} 
          thresholds={thresholds}
          cancel={() => handleCancelEdit()}
          save={() => handleSaveRole()}/>
  
      {/* ---------------- Buttons ---------------- */}
      <div className={styles.manage_roles_header}>
          <div className={styles.title_row}>
              <RiUserSettingsLine className={styles.title_icon}/>
              <h1 className={styles.page_title}>Manage Roles</h1>
          </div>
          <p className={styles.page_subtitle}>Manage roles and sensitivity thresholds for organisational data</p>
          <div className={styles.button_container}>
            <IconField iconPosition="left">
                <InputIcon className="pi pi-search"></InputIcon>
                <InputText onChange={(e) => setSearchValue(e.target.value)} style={{ width: '23vw'}} placeholder="Search by role name" className="p-inputtext-sm"/>
            </IconField>
            <Dropdown optionLabel="name" 
              placeholder="Sort by" className="p-inputtext-sm"/>
            <Button className={styles.create_role_button}>Create Role</Button>
          </div>
          
      </div>

      {/* ---------------- Role Cards ---------------- */}
      <div className={styles.card_container}>
        <div className={styles.card_header}>
          <span>Role Name</span>
          <span>Last Updated</span>
          <span>Actions</span>
        </div>
        <div className={styles.row_card_container}>
          {roles.map((role) => (
              <RoleCard name={role.name} last_updated="Placeholder" editClick={() => handleEditClick(role)}/>
          ))}
        </div>
      </div>

        {/* Right panel: Add / Edit Role */}
        {/* <div className={styles.rightPanel}>
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
        </div> */}
      </div>
  );
}

export default Roles;