import styles from "./role_card.module.css"

function RoleCard({name, last_updated, editClick}){
    return (
        <div className={styles.role_card_container}>
            <span className={styles.role_card_name}>{name}</span>
            <span className={styles.role_card_date}>{last_updated}</span>
            <div>
                <i id={styles.edit} onClick={editClick} className="pi pi-pencil"/>
                <i id={styles.delete} className="pi pi-trash"/>
                <i id={styles.ellipsis} className="pi pi-ellipsis-v"/>
            </div>
        </div>
    )
}

export default RoleCard;