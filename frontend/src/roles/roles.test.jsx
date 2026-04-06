import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import { describe, test, expect, beforeEach, vi } from "vitest";
import Roles from "./roles";
import api from "../api/axiosConfig";

// Mock API
vi.mock("../api/axiosConfig");

const mockRoles = [
  { role_id: 1, name: "Admin", role_permissions: [] },
  { role_id: 2, name: "Employee", role_permissions: [] },
];

const mockCategories = [
  { sensitivity_category_id: 1, name: "PII" },
  { sensitivity_category_id: 2, name: "Financial" },
];

const mockSubcategories = [
  { sensitivity_subcategory_id: 1, sensitivity_category_id: 1, name: "SSN" },
  { sensitivity_subcategory_id: 2, sensitivity_category_id: 2, name: "Credit Card" },
];

const mockUsers = [
  { user_id: 1, firstname: "Alice", surname: "Smith", role_id: 1, role_name: "Admin" },
  { user_id: 2, firstname: "Bob", surname: "Jones", role_id: 2, role_name: "Employee" },
];

describe("Roles Component", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();

    api.get.mockImplementation((url) => {
      switch (url) {
        case "/roles/get":
          return Promise.resolve({ data: mockRoles });
        case "/roles/sensitivity/categories":
          return Promise.resolve({ data: mockCategories });
        case "/roles/sensitivity/subcategories":
          return Promise.resolve({ data: mockSubcategories });
        case "/roles/users/all":
          return Promise.resolve({ data: mockUsers });
        default:
          return Promise.resolve({ data: [] });
      }
    });

    api.post.mockResolvedValue({
      data: { role_id: 3, name: "New Role", role_permissions: [] },
    });

    api.put.mockResolvedValue({});
    api.delete.mockResolvedValue({});
  });

  test("renders loading then roles", async () => {
    render(<Roles />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    const roles = await screen.findAllByText("Admin");
    expect(roles.length).toBeGreaterThan(0);
  });

  test("add a new role", async () => {
    render(<Roles />);

    await screen.findByText("Admin");

    fireEvent.change(screen.getByPlaceholderText("Role Name"), {
      target: { value: "New Role" },
    });

    fireEvent.click(screen.getByText("Add Role"));

    await waitFor(() => {
      expect(screen.getByText("New Role")).toBeInTheDocument();
    });
  });

  test("edit an existing role", async () => {
    render(<Roles />);

    await screen.findByText("Admin");

    fireEvent.click(screen.getAllByText("Edit")[0]);

    const input = screen.getByPlaceholderText("Role Name");

    fireEvent.change(input, {
      target: { value: "Admin Updated" },
    });

    fireEvent.click(screen.getByText("Save Changes"));

    await waitFor(() => {
      expect(api.put).toHaveBeenCalled();
    });
  });

  test("delete a role", async () => {
    render(<Roles />);

    await screen.findByText("Admin");

    fireEvent.click(screen.getAllByText("Edit")[0]);
    fireEvent.click(screen.getByText("Delete"));

    await waitFor(() => {
      expect(screen.queryByText("Admin")).not.toBeInTheDocument();
    });
  });
});