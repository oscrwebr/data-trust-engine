import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Roles from "./roles";
import api from "../api/axiosConfig";

// Mock API calls
jest.mock("../api/axiosConfig");

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
    jest.clearAllMocks();

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

    api.post.mockResolvedValue({ data: { role_id: 3, name: "New Role", role_permissions: [] } });
    api.put.mockResolvedValue({});
    api.delete.mockResolvedValue({});
  });

  test("renders loading state", () => {
    render(<Roles />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test("renders roles and users panels", async () => {
    render(<Roles />);
    // Wait for roles to load
    await waitFor(() => {
      expect(screen.getByText("Admin")).toBeInTheDocument();
      expect(screen.getByText("Employee")).toBeInTheDocument();
    });

    // Switch to User Assignment tab
    fireEvent.click(screen.getByText("User Assignment"));
    expect(screen.getByText("User Assignment")).toBeInTheDocument();
    expect(screen.getByText("Alice Smith")).toBeInTheDocument();
    expect(screen.getByText("Bob Jones")).toBeInTheDocument();
  });

  test("add a new role", async () => {
    render(<Roles />);
    await waitFor(() => screen.getByText("Admin"));

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
    await waitFor(() => screen.getByText("Admin"));

    fireEvent.click(screen.getAllByText("Edit")[0]);
    const input = screen.getByPlaceholderText("Role Name");
    fireEvent.change(input, { target: { value: "Admin Updated" } });

    fireEvent.click(screen.getByText("Save Changes"));

    await waitFor(() => {
      expect(screen.getByText("Admin Updated")).toBeInTheDocument();
    });
  });

  test("delete a role", async () => {
    render(<Roles />);
    await waitFor(() => screen.getByText("Admin"));

    fireEvent.click(screen.getAllByText("Edit")[0]);
    fireEvent.click(screen.getByText("Delete"));

    await waitFor(() => {
      expect(screen.queryByText("Admin")).not.toBeInTheDocument();
    });
  });

  test("search and filter users", async () => {
    render(<Roles />);
    await waitFor(() => screen.getByText("Admin"));

    fireEvent.click(screen.getByText("User Assignment"));

    const searchInput = screen.getByPlaceholderText("Search by username...");
    fireEvent.change(searchInput, { target: { value: "Alice" } });

    await waitFor(() => {
      expect(screen.getByText("Alice Smith")).toBeInTheDocument();
      expect(screen.queryByText("Bob Jones")).not.toBeInTheDocument();
    });

    const roleFilter = screen.getByRole("combobox");
    fireEvent.change(roleFilter, { target: { value: "2" } });

    await waitFor(() => {
      expect(screen.queryByText("Alice Smith")).not.toBeInTheDocument();
      expect(screen.getByText("Bob Jones")).toBeInTheDocument();
    });
  });

  test("assign a role to a user", async () => {
    render(<Roles />);
    await waitFor(() => screen.getByText("Alice Smith"));

    fireEvent.click(screen.getByText("User Assignment"));

    const select = screen.getAllByRole("combobox")[1]; // second select is for Alice
    fireEvent.change(select, { target: { value: "2" } });

    await waitFor(() => {
      expect(api.put).toHaveBeenCalledWith("/roles/users/1/role", { role_id: "2" });
    });
  });
});