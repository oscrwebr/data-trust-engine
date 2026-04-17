import styles from "./role_card.module.css"

function RoleCard({id, name, last_updated, editClick, deleteClick}){
    return (
        <div className={styles.role_card_container}>
            <span className={styles.role_card_name}>{name}</span>
            <span className={styles.role_card_date}>{last_updated}</span>
            <div>
                <i id={styles.edit} onClick={editClick} className="pi pi-pencil"/>
                <i id={styles.delete} onClick={deleteClick} className="pi pi-trash"/>
            </div>
        </div>
    )
}

export default RoleCard;