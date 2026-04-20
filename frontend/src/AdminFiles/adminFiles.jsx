import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
import styles from "./adminFiles.module.css";
import { useNavigate } from "react-router-dom";

function AdminFiles() {
  const navigate = useNavigate();

  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState([]);

  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);
  
  const pageSize = 10;

  const backend_uri =
    import.meta.env.VITE_BACKEND_HOST || "http://localhost:8000";

  // ✅ SAME RISK LOGIC
  const getRiskLevel = (file) => {
    if (file.invalid_access_percentage >= 50) return "high";
    if (file.invalid_access_percentage >= 25) return "medium";
    return "low";
  };

  // ✅ FETCH FILES + LAST SCANNED
  const fetchFiles = async () => {
    setLoading(true);

    try {
      const offset = (page - 1) * pageSize;

      // 1️⃣ GET BASE FILES
      const filesRes = await fetch(
        `${backend_uri}/access_mapping/get_highest_risk_files?limit=${pageSize}&offset=${offset}`
      );

      const filesData = await filesRes.json();

      const baseFiles = filesData.items || [];
      setTotal(filesData.total);

      const ids = baseFiles.map((f) => f.file_id);

      let scanMap = {};
      let graphMap = {};

      // 2️⃣ GET LAST SCANNED + GRAPH IDs
      if (ids.length > 0) {
        const scanRes = await api.get("/admin/files/last-scanned", {
          params: { file_ids: ids },
          paramsSerializer: (params) =>
            params.file_ids.map((id) => `file_ids=${id}`).join("&")
        });

        // ✅ FIX: use scanRes.data (NOT .data.data)
        scanRes.data.forEach((f) => {
          scanMap[f.file_id] = f.last_scanned;
          graphMap[f.file_id] = f.graph_file_id;
        });
      }

      // 3️⃣ MERGE EVERYTHING
      const merged = baseFiles.map((f) => ({
        ...f,
        last_scanned: scanMap[f.file_id] || null,
        graph_file_id: graphMap[f.file_id] || null
      }));

      setFiles(merged);
    } catch (err) {
      console.error("Failed to fetch files:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [page]);

  // ✅ SELECT FILES (STORE GRAPH IDS!)
  const toggleFile = (file) => {
    if (!file.graph_file_id) return;

    setSelected((prev) =>
      prev.includes(file.graph_file_id)
        ? prev.filter((id) => id !== file.graph_file_id)
        : [...prev, file.graph_file_id]
    );
  };

  // ✅ SCAN
  const scanSelected = async () => {
    if (selected.length === 0) return;

    setScanning(true);

    try {
      await api.post("/scanning/scan_files", {
        graph_file_ids: selected // ✅ CORRECT NOW
      });

      setSelected([]);
      fetchFiles();
    } catch (err) {
      console.error("Scan failed:", err);
    } finally {
      setScanning(false);
    }
  };

  // ✅ STYLING
  const getSensitivityStyle = (level) => {
    switch (level) {
      case "low":
        return { label: "Low", className: styles.low };
      case "medium":
        return { label: "Medium", className: styles.medium };
      case "high":
        return { label: "High", className: styles.high };
      default:
        return { label: "N/A", className: styles.na };
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className={styles.container}>
      <h2>Admin Files</h2>

      {/* SCAN BUTTON */}
      <button
        onClick={scanSelected}
        disabled={selected.length === 0 || scanning}
      >
        {scanning ? "Scanning..." : "Scan Selected"}
      </button>

      {/* TABLE */}
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className={styles.table}>
          <thead>
            <tr>
              <th></th>
              <th>Name</th>
              <th>Sensitivity</th>
              <th>Last Scanned</th>
              <th>Detections</th>
            </tr>
          </thead>

          <tbody>
            {files.map((file) => {
              const risk = getRiskLevel(file);
              const s = getSensitivityStyle(risk);

              return (
                <tr key={file.file_id}>
                  {/* CHECKBOX */}
                  <td>
                    <input
                      type="checkbox"
                      checked={selected.includes(file.graph_file_id)}
                      onChange={() => toggleFile(file)}
                      disabled={!file.graph_file_id}
                    />
                  </td>

                  {/* NAME */}
                  <td>
                    <span
                      className={styles.fileLink}
                      onClick={() => navigate(`/files/${file.file_id}`)}
                    >
                      {file.file_name}
                    </span>
                  </td>
                  {/* SENSITIVITY */}
                  <td>
                    <span className={`${styles.badge} ${s.className}`}>
                      {s.label}
                    </span>
                  </td>

                  {/* LAST SCANNED */}
                  <td>
                    {file.last_scanned ? (
                      new Date(file.last_scanned).toLocaleString()
                    ) : (
                      <span className={styles.neverScanned}>Never</span>
                    )}
                  </td>

                  {/* DETECTIONS */}
                  <td>{file.detection_count ?? 0}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      {/* PAGINATION */}
      <div className={styles.pagination}>
        <button
          disabled={page === 1}
          onClick={() => setPage((p) => p - 1)}
        >
          Prev
        </button>

        <span>
          Page {page} of {totalPages || 1}
        </span>

        <button
          disabled={page >= totalPages}
          onClick={() => setPage((p) => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default AdminFiles;