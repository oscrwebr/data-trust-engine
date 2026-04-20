import { OverlayPanel } from 'primereact/overlaypanel';
import styles from "./view_employees.module.css"

function MoreInformationPanel({forwardRef, risk}){
    console.log(risk["flagged_files"])
    return (
        <OverlayPanel ref={forwardRef} className={styles.overlay_container}>
            {risk.id == 1 &&(<div>
                <span className={styles.text}>We couldn't find any files related <br/>to this employee in our system.</span>
            </div>)}

            {risk.id == 2 &&(<div>
                <span className={styles.text}>This employee's files have no been scanned yet.</span>
            </div>)}

            {risk.id == 3 &&(<div>
                <span className={styles.text}>This employee has unauthorised<br/>access to the following files:</span>
                <ol style={{marginTop:'10px', paddingLeft: '0px', listStyle: 'none'}}>
                    {risk["flagged_files"].map((item, index) => (
                        <li className={styles.list_element} key={item.file.file.ingestion_file_id || index}>
                            <a href={`/files/${item.file.file.ingestion_file_id}`}>{item.file.file.name}</a>
                        </li>
                    ))}
                </ol>
            </div>)}

            {risk.id == 4 &&(<div>
                <span className={styles.text}>This employee's files are all<br/>compliant and up to date</span>
            </div>)}
        </OverlayPanel>
    )
}

export default MoreInformationPanel;