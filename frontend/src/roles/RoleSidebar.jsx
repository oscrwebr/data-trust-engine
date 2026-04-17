import { InputText } from "primereact/inputtext";
import styles from "./role_sidebar.module.css"
import { Sidebar } from "primereact/sidebar"
import SensitivityThresholdRow from "./SensitivityThresholdRow";
import { Button } from "primereact/button";

function RoleSidebar({role, visible, setVisible, categories, setThresholds, thresholds, cancel, save, onChange, editingRole}) {

    const handleThresholdChange = (subId, value) => {
        setThresholds({
        ...thresholds,
        [subId]: value === "" ? null : parseInt(value, 10),
        });
    };

    return (
        <Sidebar className={styles.sidebar} header={<h2 className={styles.header}>{editingRole ? "Edit Role" : "Create Role"}</h2>} visible={visible} position="right" onHide={() => setVisible()}>
            <div className={styles.sidebar_container}> 
                <div className={styles.basic_information}>
                    <span className={styles.title}>Basic Information</span>
                    <span className={styles.label}>Role Name</span>
                    <InputText className={styles.role_input} value={editingRole ? role : null} placeholder={editingRole ? "" : "Enter the name of the role"} onChange={onChange}/>
                </div>
                <div className={styles.sensitivity_thresholds}>
                    <span className={styles.title}>Sensitivity Thresholds</span>
                    <span className={styles.label}>Set sensitivity levels (0-50) for different data types</span>
                    {categories.map((category) => (
                        <div key={category.sensitivity_category_id}>
                        <div className={styles.sensitivity_threshold_container}>{category.name}
                            {category.subcategories.map((subcategory) => (
                                <SensitivityThresholdRow 
                                    subcategory={subcategory.name}
                                    value={thresholds[subcategory.sensitivity_subcategory_id]}
                                    setInputValue={(e) => handleThresholdChange (
                                            subcategory.sensitivity_subcategory_id,
                                            e.target.value
                                        )
                                    }

                                    setSliderValue={(e) => handleThresholdChange (
                                            subcategory.sensitivity_subcategory_id,
                                            e.value
                                        )
                                    }
                                />
                            ))}
                        </div>
                        </div>
                    ))}         
                </div>
            </div>
            <div className={styles.footer}>
                <Button className={styles.cancel_button} label="Cancel" onClick={cancel}/>
                <Button className={styles.save_changes_button} label={editingRole ? "Save Changes" : "Create Role"} onClick={save}/>
            </div>
        </Sidebar>
    )
}

export default RoleSidebar;