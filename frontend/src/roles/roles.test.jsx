import { cleanup, render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi, beforeEach } from "vitest";
import Role from "./roles";

const mockRoles = [
  { role_id: 1, name: "Admin", role_permissions: [], last_updated:"2024-01-15 13:45:30" },
  { role_id: 2, name: "Employee", role_permissions: [], last_updated: "2024-01-15 13:50:30" },
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

vi.mock("../api/axiosConfig.js", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  },
}));

import api from "../api/axiosConfig";

describe("Role Component", () => {
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

        api.post.mockResolvedValue({});
        api.put.mockResolvedValue({});
        api.delete.mockResolvedValue({});
    });

    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });


    // Test 1
    test("Test all content in component loads correctly", async () => {
        render(
            <MemoryRouter>
                <Role/>
            </MemoryRouter>
        );

        expect(await screen.findByText("Manage Roles")).toBeInTheDocument();
        expect(await screen.findByText("Manage roles and sensitivity thresholds for organisational data")).toBeInTheDocument();
        expect(await screen.findByText("Role Name")).toBeInTheDocument();
        expect(await screen.findByText("Last Updated")).toBeInTheDocument();
        expect(await screen.findByText("Actions")).toBeInTheDocument();
        const rows = await screen.findAllByTestId("role-card");
        expect(rows.length).toBe(2);

    });

    // Test 2
    test("Check that search bar works as expected and returns correct row", async() => {

        render(
            <MemoryRouter>
                <Role />
            </MemoryRouter>
        );

        const search = await screen.findByPlaceholderText("Search by role name");
        fireEvent.change(search, { target: { value: "a" } });

        expect(await screen.findByText("Admin")).toBeInTheDocument();
        expect(screen.queryByText("Employee")).not.toBeInTheDocument();
    })

    // Test 3
    test("Test full use case for creating a new role", async() => {
        api.post.mockResolvedValue({
            data: {
                role_id: 3,
                name: "New Role",
                last_updated: "2024-01-15 13:55:00",
                role_permissions: []
            }
        });

        render(
            <MemoryRouter>
                <Role />
            </MemoryRouter>
        );

        const create_button = await screen.findByText("Create Role");
        fireEvent.click(create_button);

        const input = screen.getByPlaceholderText("Enter the name of the role");
        fireEvent.change(input, { target: { value: "New Role" } });

        const create_button_2 = await screen.findByTestId("submit-button");
        fireEvent.click(create_button_2);

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith(
                '/roles/create',
                {
                    name: "New Role",
                    thresholds: [],
                }
            );
        });
        
        expect(await screen.findByText("New Role")).toBeInTheDocument();
    })

    // Test 4
    test("Test full use case for updating an existing role", async() => {

        api.put.mockResolvedValue({
            data: {
                role_id: 1,
                name: "New Role",
                last_updated: "2024-01-15 13:55:00",
                role_permissions: []
            }
        });

        render(
            <MemoryRouter>
                <Role />
            </MemoryRouter>
        );

        const edit_button = await screen.findAllByTestId("edit-button");
        fireEvent.click(edit_button[0]);

        const input = await screen.findByTestId("role-input")
        fireEvent.change(input, { target: { value: "New Role" } });

        const save_changes_button = await screen.findByTestId("submit-button");
        fireEvent.click(save_changes_button);

        await waitFor(() => {
            expect(api.put).toHaveBeenCalledWith(
                '/roles/update/1',
                {
                    name: "New Role",
                    thresholds: [],
                }
            );
        });
    })

    // Test 5
    test("Test full use case for deleting a role", async() => {

        render(
            <MemoryRouter>
                <Role />
            </MemoryRouter>
        );

        const delete_button = await screen.findAllByTestId("delete-button");
        fireEvent.click(delete_button[0]);

        const delete_button_modal = await screen.findByTestId("delete-button-modal");
        fireEvent.click(delete_button_modal);

        await waitFor(() => {
            expect(api.delete).toHaveBeenCalledWith(
                '/roles/delete/1'
            );
        });
    
        await waitFor(() => {
            expect(screen.queryByText("Admin")).not.toBeInTheDocument();
        });
    })
});