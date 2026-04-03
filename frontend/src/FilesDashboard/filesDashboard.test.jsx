import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, test, expect, beforeEach, vi } from "vitest";
import FilesDashboard from "./filesDashboard";
import api from "../api/axiosConfig";

vi.mock("react-icons/fa", () => ({
  FaFile: () => <span>FaFile</span>,
  FaFilePdf: () => <span>FaFilePdf</span>,
  FaFileWord: () => <span>FaFileWord</span>,
  FaFileExcel: () => <span>FaFileExcel</span>,
  FaFilePowerpoint: () => <span>FaFilePowerpoint</span>,
  FaFileImage: () => <span>FaFileImage</span>,
  FaFileAudio: () => <span>FaFileAudio</span>,
  FaFileVideo: () => <span>FaFileVideo</span>,
  FaFileCode: () => <span>FaFileCode</span>,
  FaFileArchive: () => <span>FaFileArchive</span>,
}));

// Mock API
vi.mock("../api/axiosConfig");

const mockRootFolders = [
  { folder_id: "1", graph_id: "g1", name: "Folder 1" },
  { folder_id: "2", graph_id: "g2", name: "Folder 2" },
];

const mockSubfolders = [
  { folder_id: "3", graph_id: "g3", name: "Subfolder 1" },
];

const mockFiles = [
  { file_id: "f1", ingestion_file_id: "i1", file_name: "file1.pdf", extension: "pdf" },
];

describe("FilesDashboard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("renders loading state initially", () => {
    api.get.mockResolvedValue({ data: [] });
    render(
      <MemoryRouter>
        <FilesDashboard />
      </MemoryRouter>
    );
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test("renders root folders", async () => {
    api.get.mockResolvedValueOnce({ data: mockRootFolders });
  
    render(
      <MemoryRouter>
        <FilesDashboard />
      </MemoryRouter>
    );
  
    await waitFor(() => {
      expect(
        screen.getByText((content) => content.includes("Folder 1"))
      ).toBeInTheDocument();
      expect(
        screen.getByText((content) => content.includes("Folder 2"))
      ).toBeInTheDocument();
    });
  });
  
  test("expands folder and loads children", async () => {
    api.get.mockResolvedValueOnce({ data: mockRootFolders }); // root
    api.get.mockImplementation((url) => {
      if (url === "/files/folders/g1") return Promise.resolve({ data: mockSubfolders });
      if (url === "/files/g1") return Promise.resolve({ data: mockFiles });
    });
  
    render(
      <MemoryRouter>
        <FilesDashboard />
      </MemoryRouter>
    );
  
    const folder1 = await screen.findByText((content) => content.includes("Folder 1"));
  
    fireEvent.click(folder1);
  
    await waitFor(() => {
      expect(screen.getByText((content) => content.includes("Subfolder 1"))).toBeInTheDocument();
      expect(screen.getByText((content) => content.includes("file1.pdf"))).toBeInTheDocument();
      expect(screen.getByText("FaFilePdf")).toBeInTheDocument();
    });
  });

  test("shows error message on API failure", async () => {
    api.get.mockRejectedValueOnce(new Error("API error"));

    render(
      <MemoryRouter>
        <FilesDashboard />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/failed to fetch root folders/i)).toBeInTheDocument();
    });
  });

  test("shows 'no files or folders' when empty", async () => {
    api.get.mockResolvedValueOnce({ data: [] });

    render(
      <MemoryRouter>
        <FilesDashboard />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/no files or folders found/i)).toBeInTheDocument();
    });
  });
});