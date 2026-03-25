import { Avatar } from "primereact/Avatar";
import styles from "./employees.module.css"
import { Button } from "primereact/button";

function RowCard({initials, firstname, surname, email, role}){
    return(
        <div className={styles.row_card_container}>
            <Avatar label={initials} size="large" shape="circle" />
            <span>{firstname} {surname}</span>
            <span>{email}</span>
            <span>{role}</span>
            <span>Some sort of scanning flag e.g. they're a risk</span>
            <Button>Send a message</Button>
        </div>
    )
}

export default RowCard;