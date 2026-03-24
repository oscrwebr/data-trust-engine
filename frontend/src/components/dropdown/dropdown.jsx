import { useState } from "react";
import styles from "./dropdown.module.css"

function SidebarDropdown({icon, label, children, openDropdown, setOpenDropdown}){

    const isOpen = openDropdown === label;

    // Logic to determine whether the dropdown is opened or closed
    const toggle = () => {
      if (isOpen) {
        setOpenDropdown(null);
      } else {
        setOpenDropdown(label); 
      }
    };

    return (
        <div className={styles.dropdown_container}>
            <div className={styles.dropdown_button} tabIndex={0} onClick={toggle}>
              <i id={styles.dropdown_icon} className={icon} />
              <span>{label}</span>
              <i id={styles.dropdown_chevron} className={isOpen ? "pi pi-angle-down" : "pi pi-angle-right"}/>
            </div>

            {isOpen && (
              <div>
                <div>{children}</div>
              </div>
            )}
        </div>
    )   
}

export default SidebarDropdown; 