import { useEffect, useState } from "react";
import api from "../../api/axiosConfig";

function Roles() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchRoles() {
      try {
        const response = await api.get("/roles/get");
        setRoles(response.data);
      } catch (err) {
        console.error("Error fetching roles:", err);
        setError("Failed to fetch roles");
      } finally {
        setLoading(false);
      }
    }

    fetchRoles();
  }, []);

  if (loading) return <p>Loading roles...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Roles</h1>
      {roles.length === 0 ? (
        <p>No roles found.</p>
      ) : (
        <ul>
          {roles.map((role) => (
            <li key={role.id}>{role.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Roles;
