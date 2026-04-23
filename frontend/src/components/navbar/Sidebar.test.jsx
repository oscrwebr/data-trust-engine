import Sidebar from "./Sidebar";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

import api from "../../api/axiosConfig";

vi.mock("../../api/axiosConfig");

describe("Sidebar Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    beforeEach(() => {
        api.get.mockResolvedValue({
            data: new Blob(["fake"], { type: "image/png" }),
        });
    });

    // Test 1
    test("All information is correctly displayed in the sidebar when an admin logs in", async() => {
        
        render(
            <MemoryRouter>
                <Sidebar 
                    setSidebarVisible={vi.fn()}
                    firstname="John"
                    surname="Smith"
                    email="test@example.com"
                    setVisible={true} 
                    role="admin"
                />
            </MemoryRouter>
            
        );

        expect(screen.getByText("John Smith")).toBeInTheDocument();
        expect(screen.getByText("Admin")).toBeInTheDocument();
        expect(screen.getByText("My Employees")).toBeInTheDocument();
        expect(screen.getByText("Configure")).toBeInTheDocument();
        expect(screen.getByText("Scanning")).toBeInTheDocument();
        expect(screen.getByText("test@example.com")).toBeInTheDocument();
        expect(screen.getByText("Dashboard")).toBeInTheDocument();
        expect(screen.getByText("Sign-out")).toBeInTheDocument();
    })

    // Test 2
    test("All information is correctly displayed in the sidebar when an employee logs in", async() => {
        
        render(
            <MemoryRouter>
                <Sidebar 
                    setSidebarVisible={vi.fn()}
                    firstname="John"
                    surname="Smith"
                    email="test@example.com"
                    setVisible={true} 
                    role="employee"
                />
            </MemoryRouter>
        );

        expect(screen.getByText("John Smith")).toBeInTheDocument();
        expect(screen.getByText("Employee")).toBeInTheDocument();
        expect(screen.queryByText("My Employees")).not.toBeInTheDocument();
        expect(screen.queryByText("Configure")).not.toBeInTheDocument();
        expect(screen.queryByText("Scanning")).not.toBeInTheDocument();
        expect(screen.getByText("test@example.com")).toBeInTheDocument();
        expect(screen.getByText("Dashboard")).toBeInTheDocument();
        expect(screen.getByText("Sign-out")).toBeInTheDocument();
    })

    // Test 3
    test("Test that when sidebar close button is clicked, the sidebar disappears", async() => {
        const mockSetSidebarVisible = vi.fn();

        render(
            <MemoryRouter>
                <Sidebar 
                    setSidebarVisible={mockSetSidebarVisible}
                    firstname="John"
                    surname="Smith"
                    email="test@example.com"
                    setVisible={true} 
                    role="employee"
                />
            </MemoryRouter>
        );

        const close_button = screen.getByTestId("close-button")
        fireEvent.click(close_button);

        expect(mockSetSidebarVisible).toHaveBeenCalledWith(false);
    })

    // Test 4
    test("Check that correct badge number displays to indicate number of pending employees", async () => {
        const pendingEmployeesMock = [
            { id: 1, name: "Alice" },
            { id: 2, name: "Bob" },
            { id: 3, name: "Charlie" },
        ];

        api.get.mockImplementation((url) => {
        if (url === "/workspace/get-workspace-image") {
            return Promise.resolve({ data: new Blob(["image"]) });
        }
        return Promise.resolve({ data: [] });
        });

        // Render Sidebar
        render(
        <MemoryRouter>
            <Sidebar
            setSidebarVisible={vi.fn()}
            firstname="John"
            surname="Smith"
            email="test@example.com"
            setVisible={vi.fn()}
            role="admin"
            pendingEmployees={pendingEmployeesMock}
            />
        </MemoryRouter>
        );

        // Wait for the "My Employees" dropdown clickable div to appear
        const myEmployeesDropdown = await screen.findByTestId("my-employees-element");

        // Click it to expand
        await userEvent.click(myEmployeesDropdown);

        // The "Manage Employees" DropdownItem should render the badge
        const badge = await screen.findByText(pendingEmployeesMock.length.toString());

        expect(badge).toBeInTheDocument();
    });
})