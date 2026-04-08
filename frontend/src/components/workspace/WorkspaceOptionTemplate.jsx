import { Avatar } from "primereact/avatar";
import styles from "./workspace.module.css"

function WorkspaceOptionTemplate({ workspace }) {
  if (!workspace) return <span>Select a workspace</span>;

  const backend_uri = import.meta.env.VITE_BACKEND_HOST || "http://localhost:8000"
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
      <Avatar
        key={workspace.id}
        image={`${backend_uri}/workspace/image/${workspace.id}`}
        shape="circle"
      />
      <span>{workspace.name}</span>
    </div>
  );
}

export default WorkspaceOptionTemplate;