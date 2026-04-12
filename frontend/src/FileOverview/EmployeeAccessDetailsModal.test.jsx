import { describe, test, expect, vi, afterEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import EmployeeAccessDetailsModal from "./EmployeeAccessDetailsModal";

describe("EmployeeAccessDetailModalTests", () => {

    // Cleanup after each test
    afterEach(() => {
        cleanup();
    })


    // Test to ensure employee details are rendered
    test("employeeAccessDetailsModalRendersEmployeeDetails", () => {
        const employee = {
            user_id: 1,
            name: "Test Employee",
            email: "testemployee@test.com",
            roles: ["PII Role"],
            access_allowed: false,
            failed_detections: [
                {
                    subcategory: "CITATION",
                    count: 14,
                    threshold: 5
                }
            ]
        };

        render(
            <EmployeeAccessDetailsModal
                employee={employee}
                onClose={vi.fn()}
            />
        );

        expect(screen.getByText("Test Employee")).toBeInTheDocument();
        expect(screen.getByText("testemployee@test.com")).toBeInTheDocument();
        expect(screen.getByText("PII Role")).toBeInTheDocument();
        expect(screen.getByText(/This file contains/i)).toBeInTheDocument();
    });


    // Test to ensure failed detections table is rendered
    test("employeeAccessDetailsModalRendersFailedDetectionsTable", () => {
        const employee = {
            user_id: 1,
            name: "Test Employee",
            email: "testemployee@test.com",
            roles: ["PII Role"],
            access_allowed: false,
            failed_detections: [
                {
                    subcategory: "CITATION",
                    count: 14,
                    threshold: 5
                },
                {
                    subcategory: "CASE_NAME",
                    count: 3,
                    threshold: 0
                }
            ]
        };

        render(
            <EmployeeAccessDetailsModal
                employee={employee}
                onClose={vi.fn()}
            />
        );

        expect(screen.getByText("Data Type")).toBeInTheDocument();
        expect(screen.getByText("Occurrences")).toBeInTheDocument();
        expect(screen.getByText("Threshold")).toBeInTheDocument();

        expect(screen.getByText("CITATION")).toBeInTheDocument();
        expect(screen.getByText("CASE_NAME")).toBeInTheDocument();
        expect(screen.getByText("14")).toBeInTheDocument();
        expect(screen.getByText("3")).toBeInTheDocument();
        expect(screen.getByText("Maximum 5")).toBeInTheDocument();
        expect(screen.getByText("Not permitted")).toBeInTheDocument();
    });
})