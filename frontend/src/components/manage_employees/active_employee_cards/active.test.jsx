import { afterEach, describe, expect, test, vi } from "vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import ActiveEmployeeRow from "./ActiveEmployeeRow";
import ActiveEmployeeSquare from "./ActiveEmployeeSquare";

const roles = [{ name: "Role" }];

describe("Active Employee Components", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Check that all elements for active employee row card load as expected", async() => {

        render(
            <MemoryRouter>
                <ActiveEmployeeRow initials="TC" firstname="Test" surname="Case" email="test@email.com" employeeRole="Role" roles={roles}/>
            </MemoryRouter>
        );

        expect(await screen.findByText("TC")).toBeInTheDocument();
        expect(await screen.findByText(/Test/)).toBeInTheDocument();
        expect(await screen.findByText(/Case/)).toBeInTheDocument();
        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        const dropdown = screen.getByTestId("row-role-dropdown");
        const label = dropdown.querySelector(".p-dropdown-label");
        expect(within(label).getByText("Role")).toBeInTheDocument();
        expect(await screen.findByText("Remove")).toBeInTheDocument();
    })

    // Test 2
    test("Check that all elements for active employee square card load as expected", async() => {
        render(
            <MemoryRouter>
                <ActiveEmployeeSquare initials="TC" firstname="Test" surname="Case" email="test@email.com" employeeRole="Role" roles={roles}/>
            </MemoryRouter>
        );

        expect(await screen.findByText("TC")).toBeInTheDocument();
        expect(await screen.findByText(/Test/)).toBeInTheDocument();
        expect(await screen.findByText(/Case/)).toBeInTheDocument();
        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        const dropdown = screen.getByTestId("square-role-dropdown");
        const label = dropdown.querySelector(".p-dropdown-label");
        expect(label).toHaveTextContent("Role");
        expect(await screen.findByTestId("remove-icon-button")).toBeInTheDocument();
    })

})