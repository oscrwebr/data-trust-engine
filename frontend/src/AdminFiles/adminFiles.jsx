import { useEffect, useState, useMemo } from "react";
import api from "../api/axiosConfig";
import styles from "./adminFiles.module.css";
import { useNavigate } from "react-router-dom";

function AdminFiles() {
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState([]);

  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);

  // 🔎 SEARCH + SORT STATE
  const [search, setSearch] = useState("");
  const [sensitivityFilter, setSensitivityFilter] = useState("all");
  const [sortBy, setSortBy] = useState("risk");

  const pageSize = 10;

  const backend_uri =
    import.meta.env.VITE_BACKEND_HOST || "http://localhost:8000";

  const navigate = useNavigate();

  // ----------------------------
  // RISK LOGIC (UNCHANGED)
  // ----------------------------
  const getRiskLevel = (file) => {
    if (file.invalid_access_percentage >= 50) return "high";
    if (file.invalid_access_percentage >= 25) return "medium";
    return "low";
  };

  // ----------------------------
  // FETCH DATA
  // ----------------------------
  const fetchFiles = async () => {
    setLoading(true);

    try {
      const offset = (page - 1) * pageSize;

      const res = await fetch(
        `${backend_uri}/admin/files/get_highest_risk_files?limit=${pageSize}&offset=${offset}`
      );

      const data = await res.json();

      setFiles(data.items || []);
      setTotal(data.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [page]);

  // ----------------------------
  // SELECT FILES
  // ----------------------------
  const toggleFile = (fileId) => {
    setSelected((prev) =>
      prev.includes(fileId)
        ? prev.filter((id) => id !== fileId)
        : [...prev, fileId]
    );
  };

  // ----------------------------
  // SCAN
  // ----------------------------
  const scanSelected = async () => {
    if (selected.length === 0) return;

    setScanning(true);

    try {
      await api.post("/scanning/scan_files", {
        graph_file_ids: selected
      });

      setSelected([]);
      fetchFiles();
    } catch (err) {
      console.error(err);
    } finally {
      setScanning(false);
    }
  };

  // ----------------------------
  // SENSITIVITY LABEL
  // ----------------------------
  const getSensitivity = (file) => {
    const risk = getRiskLevel(file);

    if (risk === "high") return "high";
    if (risk === "medium") return "medium";
    return "low";
  };

  // ----------------------------
  // FILTER + SORT (CLIENT SIDE)
  // ----------------------------
  const filteredAndSortedFiles = useMemo(() => {
    let result = [...files];

    // 🔎 SEARCH BY NAME
    if (search.trim()) {
      result = result.filter((f) =>
        f.file_name.toLowerCase().includes(search.toLowerCase())
      );
    }

    // 🎯 FILTER BY SENSITIVITY
    if (sensitivityFilter !== "all") {
      result = result.filter(
        (f) => getSensitivity(f) === sensitivityFilter
      );
    }

    // ↕️ SORTING
    result.sort((a, b) => {
      switch (sortBy) {
        case "name":
          return a.file_name.localeCompare(b.file_name);

        case "sensitivity":
          return (
            getRiskLevel(b) - getRiskLevel(a)
          );

        case "detections":
          return b.detection_count - a.detection_count;

        case "last_scanned":
          return new Date(b.last_scanned || 0) - new Date(a.last_scanned || 0);

        default:
          return 0;
      }
    });

    return result;
  }, [files, search, sensitivityFilter, sortBy]);

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className={styles.container}>
      <h2>Admin Files</h2>

      {/* ---------------- FILTER BAR ---------------- */}
      <div className={styles.filters}>
        <input
          placeholder="Search file name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          value={sensitivityFilter}
          onChange={(e) => setSensitivityFilter(e.target.value)}
        >
          <option value="all">All Sensitivity</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>

        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="risk">Default (Risk)</option>
          <option value="name">Name</option>
          <option value="sensitivity">Sensitivity</option>
          <option value="last_scanned">Last Scanned</option>
          <option value="detections">Detections</option>
        </select>
      </div>

      {/* ---------------- SCAN BUTTON ---------------- */}
      <button
        onClick={scanSelected}
        disabled={selected.length === 0 || scanning}
      >
        {scanning ? "Scanning..." : "Scan Selected"}
      </button>

      {/* ---------------- TABLE ---------------- */}
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
            {filteredAndSortedFiles.map((file) => {
              const sensitivity = getSensitivity(file);

              return (
                <tr key={file.file_id}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selected.includes(file.file_id)}
                      onChange={() => toggleFile(file.file_id)}
                    />
                  </td>

                  {/* clickable name */}
                  <td
                    className={styles.fileLink}
                    onClick={() => navigate(`/files/${file.file_id}`)}
                  >
                    {file.file_name}
                  </td>

                  <td>{sensitivity}</td>

                  <td>
                    {file.last_scanned
                      ? new Date(file.last_scanned).toLocaleString()
                      : "Never"}
                  </td>

                  <td>{file.detection_count}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      {/* ---------------- PAGINATION ---------------- */}
      <div className={styles.pagination}>
        <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>
          Prev
        </button>

        <span>
          Page {page} of {totalPages || 1}
        </span>

        <button
          disabled={page >= totalPages}
          onClick={() => setPage(p => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default AdminFiles;