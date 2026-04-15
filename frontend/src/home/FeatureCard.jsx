import styles from "./feature_card.module.css"

function FeatureCard({icon, title, description, bullet_1, bullet_2, bullet_3}){
    return(
        <div className={styles.container}>
          <i id={styles.icon} className={icon}/>
          <span className={styles.title}>{title}</span>
          <span className={styles.description}>{description}</span>
          <div className={styles.bullet_container}>
            <div className={styles.bullet}>
              <i className="pi pi-check-circle"/>
              <span>{bullet_1}</span>
            </div>
            <div className={styles.bullet}>
              <i className="pi pi-check-circle"/>
              <span>{bullet_2}</span>
            </div>
            <div className={styles.bullet}>
              <i className="pi pi-check-circle"/>
              <span>{bullet_3}</span>
            </div>
          </div>
        </div>
    )
}

export default FeatureCard;