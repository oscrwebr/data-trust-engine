import { describe, test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import EmployeeAccessItem from "./EmployeeAccessItem";


describe("EmployeeAccessItemTests", () => {
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
    })
})