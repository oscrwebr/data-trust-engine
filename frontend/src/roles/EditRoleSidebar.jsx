import { InputText } from "primereact/inputtext";
import styles from "./edit_role_sidebar.module.css"
import { Sidebar } from "primereact/sidebar"
import { Slider } from "primereact/slider";
import SensitivityThresholdRow from "./SensitivityThresholdRow";
import { Button } from "primereact/button";

function EditRoleSidebar({role, visible, setVisible, categories, setThresholds, thresholds, cancel, save}) {

    const handleThresholdChange = (subId, value) => {
        setThresholds({
        ...thresholds,
        [subId]: value === "" ? null : parseInt(value, 10),
        });
    };

    return (
        <Sidebar className={styles.sidebar} header="Edit Role" visible={visible} position="right" onHide={() => setVisible(false)}>
            <div>
                <span>Basic Information</span>
                <span>Role Name</span>
                <InputText value={role?.name}/>
            </div>
            <div>
                <span>Sensitivity Thresholds</span>
                <span>Set sensitivity levels (0-50) for different data types</span>
                {categories.map((category) => (
                    <div key={category.sensitivity_category_id}>
                    <div className={styles.sensitivityCategory}>{category.name}</div>
                    {category.subcategories.map((subcategory) => (
                        <SensitivityThresholdRow 
                            subcategory={subcategory.name}
                            value={thresholds[subcategory.sensitivity_subcategory_id] ?? 0}
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
                ))}
                <div>
                    <Button label="Cancel" onClick={cancel}/>
                    <Button label="Save Changes" onClick={save}/>
                </div>
            </div>
        </Sidebar>
    )
}

export default EditRoleSidebar;