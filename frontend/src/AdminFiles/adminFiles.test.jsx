import { afterEach, describe, expect, test, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import AdminFiles from "./adminFiles";

// ✅ mock axios api
vi.mock("../api/axiosConfig", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  },
}));

// ✅ mock navigate
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

import api from "../api/axiosConfig";

// ✅ mock global fetch (FIRST API CALL)
global.fetch = vi.fn();

describe("AdminFiles Component", () => {
  afterEach(() => {
    vi.clearAllMocks();
    cleanup();
  });

  const baseFiles = [
    {
      file_id: 1,
      file_name: "file1.txt",
      invalid_access_percentage: 60,
      detection_count: 2,
    },
    {
      file_id: 2,
      file_name: "file2.txt",
      invalid_access_percentage: 10,
      detection_count: 0,
    },
  ];

  const scanData = [
    {
      file_id: 1,
      graph_file_id: "graph-1",
      last_scanned: "2026-04-01T10:00:00",
    },
    {
      file_id: 2,
      graph_file_id: "graph-2",
      last_scanned: null,
    },
  ];

  // -------------------------------
  // Test 1: Loads + renders data
  // -------------------------------
  test("renders files with merged scan data", async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({
        items: baseFiles,
        total: 2,
      }),
    });

    api.get.mockResolvedValueOnce({
      data: scanData,
    });

    render(
      <MemoryRouter>
        <AdminFiles />
      </MemoryRouter>
    );

    expect(await screen.findByText("file1.txt")).toBeInTheDocument();
    expect(await screen.findByText("file2.txt")).toBeInTheDocument();

    // sensitivity labels
    expect(await screen.findByText("High")).toBeInTheDocument();
    expect(await screen.findByText("Low")).toBeInTheDocument();

    // last scanned
    expect(await screen.findByText(/2026/)).toBeInTheDocument();
    expect(await screen.findByText("Never")).toBeInTheDocument();
  });

  // -------------------------------
  // Test 2: Checkbox selection
  // -------------------------------
  test("selecting a file enables scan button", async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({ items: baseFiles, total: 2 }),
    });

    api.get.mockResolvedValueOnce({ data: scanData });

    render(
      <MemoryRouter>
        <AdminFiles />
      </MemoryRouter>
    );

    const checkboxes = await screen.findAllByRole("checkbox");
    const scanButton = screen.getByRole("button", { name: /scan selected/i });

    expect(scanButton).toBeDisabled();

    fireEvent.click(checkboxes[0]);

    expect(scanButton).not.toBeDisabled();
  });

  // -------------------------------
  // Test 3: Scan API call
  // -------------------------------
  test("scan button calls API with selected graph ids", async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({ items: baseFiles, total: 2 }),
    });

    api.get.mockResolvedValueOnce({ data: scanData });
    api.post.mockResolvedValueOnce({ data: {} });

    render(
      <MemoryRouter>
        <AdminFiles />
      </MemoryRouter>
    );

    const checkboxes = await screen.findAllByRole("checkbox");
    fireEvent.click(checkboxes[0]);

    const button = screen.getByText("Scan Selected");
    fireEvent.click(button);

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith("/scanning/scan_files", {
        graph_file_ids: ["graph-1"],
      });
    });
  });

  // -------------------------------
  // Test 4: Navigation works
  // -------------------------------
  test("clicking file name navigates correctly", async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({ items: baseFiles, total: 2 }),
    });

    api.get.mockResolvedValueOnce({ data: scanData });

    render(
      <MemoryRouter>
        <AdminFiles />
      </MemoryRouter>
    );

    const fileLink = await screen.findByText("file1.txt");
    fireEvent.click(fileLink);

    expect(mockNavigate).toHaveBeenCalledWith("/files/1");
  });

  // -------------------------------
  // Test 5: Pagination next page
  // -------------------------------
  test("pagination next button loads next page", async () => {
    fetch
      .mockResolvedValueOnce({
        json: async () => ({ items: baseFiles, total: 20 }),
      })
      .mockResolvedValueOnce({
        json: async () => ({ items: [], total: 20 }),
      });

    api.get.mockResolvedValue({ data: scanData });

    render(
      <MemoryRouter>
        <AdminFiles />
      </MemoryRouter>
    );

    const nextButton = await screen.findByText("Next");
    fireEvent.click(nextButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(2);
    });
  });

  // -------------------------------
  // Test 6: Loading state
  // -------------------------------
  test("shows loading state", async () => {
    fetch.mockImplementation(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                json: async () => ({ items: baseFiles, total: 2 }),
              }),
            100
          )
        )
    );

    render(
      <MemoryRouter>
        <AdminFiles />
      </MemoryRouter>
    );

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  // -------------------------------
  // Test 7: No graph_id disables checkbox
  // -------------------------------
  test("checkbox disabled when graph_file_id is null", async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({
        items: baseFiles,
        total: 2,
      }),
    });

    api.get.mockResolvedValueOnce({
      data: [
        {
          file_id: 1,
          graph_file_id: null,
          last_scanned: null,
        },
        {
          file_id: 2,
          graph_file_id: null,
          last_scanned: null,
        },
      ],
    });

    render(
      <MemoryRouter>
        <AdminFiles />
      </MemoryRouter>
    );

    const checkboxes = await screen.findAllByRole("checkbox");

    expect(checkboxes[0]).toBeDisabled();
    expect(checkboxes[1]).toBeDisabled();
  });
});