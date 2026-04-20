import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
import styles from "./adminFiles.module.css";

function AdminFiles() {
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState([]);

  const [search, setSearch] = useState("");
  const [sensitivity, setSensitivity] = useState("");
  const [sort, setSort] = useState("desc");

  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);

  const pageSize = 20;

  const fetchFiles = async () => {
    setLoading(true);

    try {
      const res = await api.get("/admin/files", {
        params: {
          search,
          sensitivity,
          sort,
          page,
          page_size: pageSize
        }
      });

      setFiles(res.data.data);
      setTotal(res.data.total);
    } catch (err) {
      console.error("Failed to fetch admin files:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [search, sensitivity, sort, page]);

  // ✅ SAFE ID RESOLVER (prevents null forever)
  const getGraphId = (file) => {
    return file?.graph_id ?? file?.file_id ?? null;
  };

  // ✅ FIXED TO NEVER STORE NULL
  const toggleFile = (file) => {
    const id = getGraphId(file);

    if (!id) {
      console.warn("Skipping file with missing ID:", file);
      return;
    }

    setSelected(prev =>
      prev.includes(id)
        ? prev.filter(x => x !== id)
        : [...prev, id]
    );
  };

  const scanSelected = async () => {
    if (selected.length === 0) return;

    // 🛑 FINAL SAFETY CHECK
    const cleaned = selected.filter(id => id != null);

    if (cleaned.length === 0) {
      console.warn("No valid graph_file_ids to scan");
      return;
    }

    setScanning(true);

    try {
      await api.post("/scanning/scan_files", {
        graph_file_ids: cleaned
      });

      setSelected([]);
      fetchFiles();
    } catch (err) {
      console.error("Scan failed:", err);
    } finally {
      setScanning(false);
    }
  };

  const getSensitivityStyle = (value) => {
    switch (value?.toLowerCase()) {
      case "safe":
        return { label: "Safe", className: styles.safe };
      case "low":
        return { label: "Low", className: styles.low };
      case "medium":
        return { label: "Medium", className: styles.medium };
      case "high":
        return { label: "High", className: styles.high };
      case "critical":
        return { label: "Critical", className: styles.high };
      default:
        return { label: "N/A", className: styles.na };
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className={styles.container}>
      <h2>Admin Files</h2>

      {/* Filters */}
      <div className={styles.filters}>
        <input
          placeholder="Search files..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
        />

        <select
          value={sensitivity}
          onChange={(e) => {
            setSensitivity(e.target.value);
            setPage(1);
          }}
        >
          <option value="">All</option>
          <option value="safe">Safe</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>

        <select
          value={sort}
          onChange={(e) => {
            setSort(e.target.value);
            setPage(1);
          }}
        >
          <option value="desc">Most Recent</option>
          <option value="asc">Least Recent</option>
        </select>
      </div>

      {/* Scan button */}
      <button
        onClick={scanSelected}
        disabled={selected.length === 0 || scanning}
      >
        {scanning ? "Scanning..." : "Scan Selected"}
      </button>

      {/* Table */}
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
              const id = getGraphId(file);
              const s = getSensitivityStyle(file.sensitivity);

              return (
                <tr key={id ?? file.name}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selected.includes(id)}
                      onChange={() => toggleFile(file)}
                      disabled={!id}
                    />
                  </td>

                  <td>{file.name}</td>

                  <td>
                    <span className={`${styles.badge} ${s.className}`}>
                      {s.label}
                    </span>
                  </td>

                  <td>
                    {file.last_scanned
                      ? new Date(file.last_scanned).toLocaleString()
                      : "Never"}
                  </td>

                  <td>{file.detections ?? 0}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      {/* Pagination */}
      <div className={styles.pagination}>
        <button
          disabled={page === 1}
          onClick={() => setPage(p => p - 1)}
        >
          Prev
        </button>

        <span>Page {page} of {totalPages || 1}</span>

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