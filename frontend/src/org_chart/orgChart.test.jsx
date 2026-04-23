import React from "react";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import { describe, test, expect, beforeEach, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import OrgChart from "./orgChart";
import api from "../api/axiosConfig";

vi.mock("../api/axiosConfig", () => ({
  default: {
    post: vi.fn(),
  },
}));

describe("OrgChart Component", () => {
  const mockToast = { current: { show: vi.fn() } };

  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  test("shows 'Upload file here' text on initial render", () => {
    render(
      <MemoryRouter>
        <OrgChart toast={mockToast} />
      </MemoryRouter>
    );

    expect(screen.getByText(/Upload file here/i)).toBeInTheDocument();
  });

  test("parses org chart and displays roles and employees", async () => {
    const fakeResponse = {
      data: {
        roles: [
          { name: "Manager", employees: [{ name: "Alice", email: "alice@example.com" }] },
          { name: "Engineer", employees: [{ name: "Bob", email: "bob@example.com" }] },
        ],
      },
    };
  
    api.post.mockResolvedValueOnce(fakeResponse);
  
    render(
      <MemoryRouter>
        <OrgChart toast={mockToast} />
      </MemoryRouter>
    );
  
    const input = document.querySelector('._fileUpload_415fd9 input[type="file"]');
    const file = new File(["dummy content"], "orgchart.csv", { type: "text/csv" });
    Object.defineProperty(input, 'files', { value: [file] });
    fireEvent.change(input);
  
    fireEvent.click(screen.getByText(/Parse Org Chart/i));
  
    await waitFor(() => {
      expect(screen.getByText("Manager")).toBeInTheDocument();
      expect(screen.getByText("Alice (alice@example.com)")).toBeInTheDocument();
      expect(screen.getByText("Engineer")).toBeInTheDocument();
      expect(screen.getByText("Bob (bob@example.com)")).toBeInTheDocument();
    });
  });
});