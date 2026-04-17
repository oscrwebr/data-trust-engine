import styles from "./role_card.module.css"
import dayjs from "dayjs";

function RoleCard({name, last_updated, editClick, deleteClick}){

    const d = dayjs(last_updated);
    const date = d.format("D MMMM YYYY");
    const time = d.format("HH:mm:ss");

    return (
        <div className={styles.role_card_container} data-testid="role-card">
            <span className={styles.role_card_name}>{name}</span>
            <span className={styles.role_card_date}>{date} at {time}</span>
            <div>
                <i id={styles.edit} onClick={editClick} className="pi pi-pencil" data-testid="edit-button"/>
                <i id={styles.delete} onClick={deleteClick} className="pi pi-trash" data-testid="delete-button"/>
            </div>
        </div>
    )
}

export default RoleCard;