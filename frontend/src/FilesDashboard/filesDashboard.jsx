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

function FilesDashboard() {
  const [tree, setTree] = useState([]);
  const [expanded, setExpanded] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // -------------------------
  // Fetch folders + files
  // -------------------------
  useEffect(() => {
    async function fetchData() {
      try {
        const [foldersRes, filesRes] = await Promise.all([
          api.get("/files/folders"),
          api.get("/files/all"),
        ]);

        const builtTree = buildTree(foldersRes.data, filesRes.data);
        setTree(builtTree);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch files and folders");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // -------------------------
  // Build Tree Structure
  // -------------------------
  const buildTree = (folders, files) => {
    const map = {};

    // init folders
    folders.forEach((f) => {
      map[f.folder_id] = {
        ...f,
        children: [],
        files: [],
      };
    });

    // link folders
    folders.forEach((f) => {
      if (f.parent_graph_id && map[f.parent_graph_id]) {
        map[f.parent_graph_id].children.push(map[f.folder_id]);
      }
    });

    // attach files
    files.forEach((file) => {
      if (map[file.parent_graph_id]) {
        map[file.parent_graph_id].files.push(file);
      }
    });

    // return root folders
    return Object.values(map).filter((f) => !f.parent_graph_id);
  };

  // -------------------------
  // File Icon Resolver
  // -------------------------
  const getFileIcon = (file) => {
    let ext = file.extension;

    // fallback if extension missing
    if (!ext && (file.file_name || file.name)) {
      const name = file.file_name || file.name;
      ext = name.split(".").pop();
    }

    ext = ext?.toLowerCase();

    // Microsoft-style specific icons
    switch (ext) {
      case "pdf":
        return <FaFilePdf color="#e74c3c" />;

      case "doc":
      case "docx":
        return <FaFileWord color="#2b579a" />;

      case "xls":
      case "xlsx":
        return <FaFileExcel color="#217346" />;

      case "ppt":
      case "pptx":
        return <FaFilePowerpoint color="#d24726" />;
      case "bat":
        return <FaFileCode color="#228B22" />;
      case "py":
        return <FaFileCode color="#3776AB" />;
    }

    // category fallback
    if (["png", "jpg", "jpeg", "gif", "bmp", "svg", "webp"].includes(ext)) {
      return <FaFileImage />;
    }

    if (["mp3", "wav", "ogg", "flac"].includes(ext)) {
      return <FaFileAudio />;
    }

    if (["mp4", "avi", "mov", "mkv"].includes(ext)) {
      return <FaFileVideo />;
    }

    if (
      [
        "js","ts","py","java","c","cpp","cs",
        "html","css","json","xml","sh","bat","ps1"
      ].includes(ext)
    ) {
      return <FaFileCode />;
    }

    if (["zip", "rar", "7z", "tar", "gz"].includes(ext)) {
      return <FaFileArchive />;
    }

    // default fallback (like Windows unknown file)
    return <FaFile />;
  };

  // -------------------------
  // Expand / Collapse
  // -------------------------
  const toggleFolder = (folderId) => {
    setExpanded((prev) => ({
      ...prev,
      [folderId]: !prev[folderId],
    }));
  };

  // -------------------------
  // Render Tree
  // -------------------------
  const renderFolder = (folder) => {
    return (
      <div key={folder.folder_id} className={styles.folder}>
        <div
          className={styles.folderHeader}
          onClick={() => toggleFolder(folder.folder_id)}
        >
          {expanded[folder.folder_id] ? "📂" : "📁"} {folder.name}
        </div>

        {expanded[folder.folder_id] && (
          <div className={styles.children}>
            {/* Subfolders */}
            {folder.children.map((child) => renderFolder(child))}

            {/* Files */}
            {folder.files.map((file) => (
              <div key={file.file_id} className={styles.file}>
                {getFileIcon(file)}
                <span>{file.file_name || file.name}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  // -------------------------
  // UI States
  // -------------------------
  if (loading) return <p className={styles.message}>Loading...</p>;
  if (error) return <p className={styles.error}>{error}</p>;

  return (
    <div className={styles.pageContainer}>
      <h2 className={styles.title}>Files & Folders</h2>

      {tree.length === 0 ? (
        <p className={styles.message}>No files or folders found</p>
      ) : (
        <div className={styles.treeContainer}>
          {tree.map((folder) => renderFolder(folder))}
        </div>
      )}
    </div>
  );
}

export default FilesDashboard;