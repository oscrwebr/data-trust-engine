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
        params: { search, sensitivity, sort, page, page_size: pageSize }
      });

      setFiles(res.data.data);
      setTotal(res.data.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [search, sensitivity, sort, page]);

  const toggleFile = (id) => {
    setSelected(prev =>
      prev.includes(id)
        ? prev.filter(f => f !== id)
        : [...prev, id]
    );
  };

  const scanSelected = async () => {
    if (selected.length === 0) return;

    setScanning(true);

    try {
      await api.post("/scanning/scan_files", {
        file_ids: selected
      });

      setSelected([]);
      fetchFiles();
    } catch (err) {
      console.error(err);
    } finally {
      setScanning(false);
    }
  };

  const getSensitivityStyle = (value) => {
    if (!value) {
      return { label: "N/A", className: styles.na };
    }
  
    switch (value.toLowerCase()) {
      case "safe":
        return { label: "Safe", className: styles.safe };
  
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

  return (
    <div className={styles.container}>
      <h2>Admin Files</h2>

      {/* 🔍 Filters */}
      <div className={styles.filters}>
        <input
          placeholder="Search files..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />

        <select onChange={e => setSensitivity(e.target.value)}>
          <option value="">All</option>
          <option value="high">High Risk</option>
          <option value="low">Low Risk</option>
        </select>

        <select onChange={e => setSort(e.target.value)}>
          <option value="desc">Most Recent</option>
          <option value="asc">Least Recent</option>
        </select>
      </div>

      {/* 🔄 Scan button */}
      <button
        onClick={scanSelected}
        disabled={selected.length === 0 || scanning}
      >
        {scanning ? "Scanning..." : "Scan Selected"}
      </button>

      {/* 📄 Table */}
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
            </tr>
          </thead>

          <tbody>
            {files.map(file => (
              <tr key={file.file_id}>
                <td>
                  <input
                    type="checkbox"
                    checked={selected.includes(file.file_id)}
                    onChange={() => toggleFile(file.file_id)}
                  />
                </td>

                <td>{file.name}</td>

                <td>
                {(() => {
                    const s = getSensitivityStyle(file.sensitivity);

                    return (
                    <span className={`${styles.badge} ${s.className}`}>
                        {s.label}
                    </span>
                    );
                })()}
                </td>
                
                <td>
                  {file.last_scanned
                    ? new Date(file.last_scanned).toLocaleString()
                    : "Never"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* 📄 Pagination */}
      <div className={styles.pagination}>
        <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>
          Prev
        </button>

        <span>Page {page}</span>

        <button
          disabled={page * pageSize >= total}
          onClick={() => setPage(p => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default AdminFiles;