import { describe, test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import EmployeeAccessItem from "./EmployeeAccessItem";


describe("EmployeeAccessItemTests", () => {
    // Test to ensure employee access item card renders employee details correctly
    test("employeeAccessItemRendersNameEmailAndRoles", () => {
        // Create a mock employee for test
        const employee = {
            user_id: 1,
            name: "Test Employee",
            email: "testemployee@test.com",
            roles: ["Test Role"],
            access_allowed: true,
            failed_detections: []
        };

        render(<EmployeeAccessItem employee={employee}/>)

        expect(screen.getByText("Test Employee")).toBeInTheDocument();
        expect(screen.getByText("testemployee@test.com")).toBeInTheDocument();
        expect(screen.getByText("Test Role")).toBeInTheDocument();
    });


    // Test to ensure employee access item card does not render any roles when employee has no roles
    test("employeeAccessItemRendersNoRolesWhenEmployeeHasNoRoles", () => {
        // Create a mock employee for test
        const employee = {
            user_id: 1,
            name: "Test Employee",
            email: "testemployee@test.com",
            roles: [],
            access_allowed: true,
            failed_detections: []
        };

        render(<EmployeeAccessItem employee={employee}/>)

        // No roles assigned message should be present
        expect(screen.getByText("No roles assigned")).toBeInTheDocument();
    });

    // Test to ensure employee access item card renders allowed icon when access is allowed
    test("employeeAccessItemRendersAllowedIcon", () => {
        // Create a mock employee for test
        const employee = {
            user_id: 1,
            name: "Test Employee",
            email: "testemployee@test.com",
            roles: ["Test Role"],
            access_allowed: true,
            failed_detections: []
        };

        const { container } = render(<EmployeeAccessItem employee={employee}/>)

        // Allowed icon should be present
        expect(container.querySelector(".allowed_icon")).toBeTruthy();
    });

    // Test to ensure employee access item card renders denied icon when access is denied
    test("employeeAccessItemRendersDeniedIcon", () => {
        // Create a mock employee for test
        const employee = {
            user_id: 1,
            name: "Test Employee",
            email: "testemployee@test.com",
            roles: ["Test Role"],
            access_allowed: false,
            failed_detections: []
        };

        const { container } = render(<EmployeeAccessItem employee={employee}/>)

        // Denied icon should be present
        expect(container.querySelector(".denied_icon")).toBeTruthy();
    });
})