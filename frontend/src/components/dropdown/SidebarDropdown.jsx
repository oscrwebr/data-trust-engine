import { useState } from "react";

function SidebarDropdown({icon, label, children}){
    const [open, setOpen] = useState(false)

    return (
        <div>
            <div onClick={() => setOpen(!open)}>
              <i className={icon} />
                <span>{label}</span>
              <i className={open ? "pi pi-angle-down" : "pi pi-angle-right"}/>
            </div>

            {open && (
              <div>
                {children}
              </div>
            )}
        </div>
    )   
}

export default SidebarDropdown; 