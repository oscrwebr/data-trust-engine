import { render, screen, fireEvent, waitFor, within, cleanup } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, test, vi, expect } from "vitest";
import Roles from "./Roles";
import api from "../api/axiosConfig";

vi.mock("../api/axiosConfig", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

afterEach(() => {
  vi.clearAllMocks();
  cleanup();
});

const mockRoles = [
  { role_id: 1, name: "Admin", role_permissions: [{ sensitivity_subcategory_id: 1, threshold: 50 }] },
  { role_id: 2, name: "User", role_permissions: [] },
];

const mockCategories = [
  { sensitivity_category_id: 1, name: "Category A" },
  { sensitivity_category_id: 2, name: "Category B" },
];

const mockSubcategories = [
  { sensitivity_subcategory_id: 1, sensitivity_category_id: 1, name: "Subcat A1" },
  { sensitivity_subcategory_id: 2, sensitivity_category_id: 1, name: "Subcat A2" },
  { sensitivity_subcategory_id: 3, sensitivity_category_id: 2, name: "Subcat B1" },
];

describe("Roles Component", () => {

  test("loads and displays existing roles and categories", async () => {
    // Mock GET responses
    api.get.mockImplementation((url) => {
      switch (url) {
        case "/roles/get":
          return Promise.resolve({ data: mockRoles });
        case "/roles/sensitivity/categories":
          return Promise.resolve({ data: mockCategories });
        case "/roles/sensitivity/subcategories":
          return Promise.resolve({ data: mockSubcategories });
      }
    });

    render(
      <MemoryRouter>
        <Roles />
      </MemoryRouter>
    );

    await waitFor(() => screen.getByText("Admin"));
    expect(screen.getByText("Admin")).toBeInTheDocument();
    expect(screen.getByText("User")).toBeInTheDocument();

    // Check categories and subcategories
    expect(screen.getByText("Category A")).toBeInTheDocument();
    expect(screen.getByText("Category B")).toBeInTheDocument();
    expect(screen.getByText("Subcat A1")).toBeInTheDocument();
    expect(screen.getByText("Subcat B1")).toBeInTheDocument();
  });

  test("adds a new role successfully", async () => {
    api.get.mockResolvedValueOnce({ data: [] });
    api.get.mockResolvedValueOnce({ data: mockCategories });
    api.get.mockResolvedValueOnce({ data: mockSubcategories });

    api.post.mockResolvedValueOnce({ data: { role_id: 3, name: "Tester", role_permissions: [] } });

    render(
      <MemoryRouter>
        <Roles />
      </MemoryRouter>
    );

    // Wait for form
    await waitFor(() => screen.getByText("Add New Role"));

    const input = screen.getByPlaceholderText("Role Name");
    fireEvent.change(input, { target: { value: "Tester" } });

    const addButton = screen.getByText("Add Role");
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith("/roles/create", {
        name: "Tester",
        thresholds: [],
      });
    });
  });

  test("edits a role and updates threshold", async () => {
    api.get.mockImplementation((url) => {
      switch (url) {
        case "/roles/get":
          return Promise.resolve({ data: mockRoles });
        case "/roles/sensitivity/categories":
          return Promise.resolve({ data: mockCategories });
        case "/roles/sensitivity/subcategories":
          return Promise.resolve({ data: mockSubcategories });
      }
    });

    api.put.mockResolvedValueOnce({ data: { role_id: 1, name: "Admin Edited" } });

    render(
      <MemoryRouter>
        <Roles />
      </MemoryRouter>
    );

    await waitFor(() => screen.getByText("Admin"));

    const editButton = screen.getAllByText("Edit")[0];
    fireEvent.click(editButton);

    const roleNameInput = screen.getByPlaceholderText("Role Name");
    fireEvent.change(roleNameInput, { target: { value: "Admin Edited" } });

    const saveButton = screen.getByText("Save Changes");
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(api.put).toHaveBeenCalledWith("/roles/update/1", {
        name: "Admin Edited",
        thresholds: [{ sensitivity_subcategory_id: 1, threshold: 50 }],
      });
    });
  });

  test("deletes a role", async () => {
    api.get.mockImplementation((url) => {
      switch (url) {
        case "/roles/get":
          return Promise.resolve({ data: mockRoles });
        case "/roles/sensitivity/categories":
          return Promise.resolve({ data: mockCategories });
        case "/roles/sensitivity/subcategories":
          return Promise.resolve({ data: mockSubcategories });
      }
    });

    api.delete.mockResolvedValueOnce({});

    render(
      <MemoryRouter>
        <Roles />
      </MemoryRouter>
    );

    await waitFor(() => screen.getByText("Admin"));

    fireEvent.click(screen.getAllByText("Edit")[0]);
    fireEvent.click(screen.getByText("Delete"));

    await waitFor(() => {
      expect(api.delete).toHaveBeenCalledWith("/roles/delete/1");
    });
  });

  test("handles empty threshold input correctly", async () => {
    api.get.mockImplementation((url) => {
      switch (url) {
        case "/roles/get":
          return Promise.resolve({ data: mockRoles });
        case "/roles/sensitivity/categories":
          return Promise.resolve({ data: mockCategories });
        case "/roles/sensitivity/subcategories":
          return Promise.resolve({ data: mockSubcategories });
      }
    });
  
    api.put.mockResolvedValueOnce({ data: { role_id: 1, name: "Admin" } });
  
    render(
      <MemoryRouter>
        <Roles />
      </MemoryRouter>
    );
  
    await waitFor(() => screen.getByText("Admin"));
  
    fireEvent.click(screen.getAllByText("Edit")[0]);
  
    const subRow = screen.getByText("Subcat A2").closest("div");
    const input = within(subRow).getByPlaceholderText("Null");
    
    fireEvent.change(input, { target: { value: "" } });
    fireEvent.click(screen.getByText("Save Changes"));

    await waitFor(() => {
      expect(api.put).toHaveBeenCalledWith("/roles/update/1", {
        name: "Admin",
        thresholds: [
          { sensitivity_subcategory_id: 1, threshold: 50 },
        ],
      });
    });
  });
});