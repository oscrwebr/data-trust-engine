import { Button } from "primereact/button";

function Notification({id, title, body, date}) {
    return (
        <div className="flex flex-column align-items-left" style={{ flex: '1' }}>
            <div className="flex align-items-center gap-2">
                <span className="font-bold text-900">{title}</span>
            </div>
            <div className="font-medium text-lg my-3 text-900">{body}</div>
            <div className="font-medium text-lg my-3 text-900">{date}</div>
        </div>
    )
}

export default Notification;