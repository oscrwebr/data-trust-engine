import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import RoleSidebar from "./RoleSidebar";

const mockRoles = [
  { role_id: 1, name: "Admin", role_permissions: [] },
];

const mockCategories = [
  { 
    sensitivity_category_id: 1, name: "PII",
    subcategories: [{ sensitivity_subcategory_id: 1, sensitivity_category_id: 1, name: "SSN" }]
  },

  { 
    sensitivity_category_id: 2, name: "Financial",
    subcategories: [{ sensitivity_subcategory_id: 2, sensitivity_category_id: 2, name: "Credit Card" }]
  },
];

describe("Role Sidebar Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });


    // Test 1
    test("Test all content in component loads correctly when editingRole is null", async () => {
        render(
            <MemoryRouter>
                <RoleSidebar role={mockRoles} visible={true} categories={mockCategories} thresholds={null} editingRole={null}/>
            </MemoryRouter>
        );

        const elements = await screen.findAllByText(/Create Role/i);
        expect(elements.length).toBeGreaterThan(0);

        expect(await screen.findByText("Basic Information")).toBeInTheDocument();
        expect(await screen.findByText("Role Name")).toBeInTheDocument();
        expect(await screen.findByText("Sensitivity Thresholds")).toBeInTheDocument();
        expect(await screen.findByText("Set sensitivity levels (0-50) for different data types")).toBeInTheDocument();
        expect(await screen.findByText("PII")).toBeInTheDocument();
        expect(await screen.findByText("Financial")).toBeInTheDocument();
        expect(await screen.findByText("SSN")).toBeInTheDocument();
        expect(await screen.findByText("Credit Card")).toBeInTheDocument();
    });
    

    // Test 2
    test("Test all content in component loads correctly when editingRole has a value", async () => {
        render(
            <MemoryRouter>
                <RoleSidebar role={mockRoles} visible={true} categories={mockCategories} thresholds={null} editingRole={mockRoles[0]}/>
            </MemoryRouter>
        );

        expect(await screen.findByText(/Edit Role/i)).toBeInTheDocument();
        expect(await screen.findByText(/Save Changes/i)).toBeInTheDocument();
        expect(await screen.findByText("Basic Information")).toBeInTheDocument();
        expect(await screen.findByText("Role Name")).toBeInTheDocument();
        expect(await screen.findByText("Sensitivity Thresholds")).toBeInTheDocument();
        expect(await screen.findByText("Set sensitivity levels (0-50) for different data types")).toBeInTheDocument();
        expect(await screen.findByText("PII")).toBeInTheDocument();
        expect(await screen.findByText("Financial")).toBeInTheDocument();
        expect(await screen.findByText("SSN")).toBeInTheDocument();
        expect(await screen.findByText("Credit Card")).toBeInTheDocument();
    });
});