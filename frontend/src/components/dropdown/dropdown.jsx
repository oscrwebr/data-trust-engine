import styles from "./dropdown.module.css"
import { useLocation } from "react-router-dom";

function SidebarDropdown({icon, label, children, openDropdown, setOpenDropdown, basePaths = [], ...props}){

    const location = useLocation();

    const isOpen = openDropdown === label;

    // Check if current route matches any child path
    const isActive = basePaths.some(path =>
      location.pathname === path || location.pathname.startsWith(path + "/")
    );

    const shouldHighlight = isActive && !isOpen;
    
    const toggle = () => {
      if (isOpen) {
        setOpenDropdown(null);
      } else {
        setOpenDropdown(label);
      }
    };


    return (
        <div className={styles.dropdown_container}>
            <div className={`${styles.dropdown_button} ${shouldHighlight ? styles.active_closed : ""}`} tabIndex={0} onClick={toggle} data-testid={props["data-testid"]} >
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