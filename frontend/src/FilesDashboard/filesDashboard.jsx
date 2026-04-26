import { useEffect, useState } from "react";
import api from "../api/axiosConfig";
import styles from "./filesDashboard.module.css";
import {
  FaFile,
  FaFilePdf,
  FaFileWord,
  FaFileExcel,
  FaFilePowerpoint,
  FaFileImage,
  FaFileAudio,
  FaFileVideo,
  FaFileCode,
  FaFileArchive
} from "react-icons/fa";
import { useNavigate } from "react-router-dom";

function FilesDashboard({ toast }) {
  const [tree, setTree] = useState([]);
  const [expanded, setExpanded] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);
  const isAdmin = user?.role === "admin";
  const [scanning, setScanning] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);

  const navigate = useNavigate();
  useEffect(() => {
    
    api.get("/workspace/dashboard")
    .then(res => {
        if (res.data.user) {
          setUser(res.data.user);
        }
    })
    .catch(error => console.log(error))

    async function fetchRoot() {
      try {
        const res = await api.get("/files/folders");

        const folders = res.data.map(f => ({
          ...f,
          children: [],
          files: [],
          childrenLoaded: false
        }));

        setTree(folders);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch root folders");
      } finally {
        setLoading(false);
      }
    }

    fetchRoot();
  }, []);

  const toggleFolder = async (folderId, graphId) => {
    setExpanded(prev => ({ ...prev, [folderId]: !prev[folderId] }));

    const folder = findFolder(tree, folderId);
    if (!folder || folder.childrenLoaded) return;

    try {
      const [subfoldersRes, filesRes] = await Promise.all([
        api.get(`/files/folders/${graphId}`),
        api.get(`/files/${graphId}`)
      ]);

      const updatedTree = updateFolder(tree, folderId, {
        children: subfoldersRes.data.map(f => ({
          ...f,
          children: [],
          files: [],
          childrenLoaded: false
        })),
        files: filesRes.data,
        childrenLoaded: true
      });

      setTree(updatedTree);
    } catch (err) {
      console.error(err);
    }
  };

  const findFolder = (folders, folderId) => {
    for (let f of folders) {
      if (f.folder_id === folderId) return f;
      if (f.children.length) {
        const found = findFolder(f.children, folderId);
        if (found) return found;
      }
    }
    return null;
  };

  const updateFolder = (folders, folderId, data) => {
    return folders.map(f => {
      if (f.folder_id === folderId) return { ...f, ...data };
      if (f.children.length)
        return { ...f, children: updateFolder(f.children, folderId, data) };
      return f;
    });
  };

  // ✅ Toggle file selection (FIXED: uses graph_id)
  const toggleFile = (graphId) => {
    console.log("TOGGLE FILE:", graphId);

    setSelectedFiles(prev =>
      prev.includes(graphId)
        ? prev.filter(id => id !== graphId)
        : [...prev, graphId]
    );
  };

  const scanSelected = async () => {
    if (!isAdmin) {
      toast.current.show({ severity: 'error', summary: 'Error', detail: 'Unauthorised.', life: 4000});
      return;
    }
  
    if (selectedFiles.length === 0) {
      toast.current.show({ severity: 'error', summary: 'Error', detail: 'No files detected.', life: 4000});
      return;
    }
  
    setScanning(true); // ✅ start spinner
  
    try {
      await api.post("/scanning/scan_files", {
        graph_file_ids: selectedFiles
      });
  
      toast.current.show({ severity: 'info', summary: 'Info', detail: 'Scanned.', life: 4000});
      setSelectedFiles([]);
    } catch (err) {
      console.error(err.response?.data || err);
            toast.current.show({ severity: 'error', summary: 'Error', detail: 'Failed to start scan.', life: 4000});
    } finally {
      setScanning(false);
      }
  };

  const getFileIcon = (file) => {
    let ext = (file.extension || (file.file_name || file.name)?.split(".").pop())?.toLowerCase();

    switch (ext) {
      case "pdf": return <FaFilePdf color="#e74c3c" />;
      case "doc":
      case "docx": return <FaFileWord color="#2b579a" />;
      case "xls":
      case "xlsx": return <FaFileExcel color="#217346" />;
      case "ppt":
      case "pptx": return <FaFilePowerpoint color="#d24726" />;
      default:
        if (["png","jpg","jpeg","gif","bmp","svg","webp"].includes(ext)) return <FaFileImage />;
        if (["mp3","wav","ogg","flac"].includes(ext)) return <FaFileAudio />;
        if (["mp4","avi","mov","mkv"].includes(ext)) return <FaFileVideo />;
        if (["js","ts","py","java","c","cpp","cs","html","css","json","xml","sh","bat","ps1"].includes(ext)) return <FaFileCode />;
        if (["zip","rar","7z","tar","gz"].includes(ext)) return <FaFileArchive />;
        return <FaFile />;
    }
  };

  const renderFolder = (folder) => (
    <div key={folder.folder_id} className={styles.folder}>
      
      {/* Folder header (NO checkbox) */}
      <div
        className={styles.folderHeader}
        onClick={() => toggleFolder(folder.folder_id, folder.graph_id)}
      >
        {expanded[folder.folder_id] ? "📂" : "📁"} {folder.name}
      </div>

      {expanded[folder.folder_id] && (
        <div className={styles.children}>
          {folder.children.map(renderFolder)}

          {folder.files.map(file => (
            <div
              key={file.file_id}
              className={`${styles.file} ${file.is_shared ? styles.sharedFile : ""}`}
            >
              {isAdmin && (
                <input
                  type="checkbox"
                  checked={selectedFiles.includes(file.graph_id)}
                  onChange={() => toggleFile(file.graph_id)}
                  onClick={(e) => e.stopPropagation()}
                />
              )}

              <div
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/files/${file.ingestion_file_id}`);
                }}
              >
                {getFileIcon(file)}
                <span>{file.file_name || file.name}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  if (loading) return <p className={styles.message}>Loading...</p>;
  if (error) return <p className={styles.error}>{error}</p>;

  return (
    <div className={styles.pageContainer}>
      <div>
        <div className={styles.header_container}>
          <i id={styles.header_icon} className="pi pi-folder"/>
          <h2 className={styles.title}>Files & Folders</h2>
        </div>
        <div>
          {isAdmin && (
            <button
              onClick={scanSelected}
              disabled={selectedFiles.length === 0 || scanning}
              className={styles.scanButton}
            >
              {scanning ? (
                <>
                  <span className={styles.spinner}></span> Scanning...
                </>
              ) : (
                "Scan Selected Files"
              )}
            </button>
          )}
        </div>
      </div>
      
      {tree.length === 0 ? (
        <p className={styles.message}>No files or folders found</p>
      ) : (
        <div className={styles.treeContainer}>
          {tree.map(renderFolder)}
        </div>
      )}
    </div>
  );
}

export default FilesDashboard;