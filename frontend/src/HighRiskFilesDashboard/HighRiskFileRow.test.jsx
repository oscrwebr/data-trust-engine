import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, vi, beforeEach, afterEach, test, expect } from "vitest";

import HighRiskFileRow from "./HighRiskFileRow";

const mock_navigate = vi.fn();

// Mock the react router to use the mock navigate
vi.mock("react-router-dom", async () => {
    const actual = await vi.importActual("react-router-dom");
    return {
        ...actual,
        useNavigate: () => mock_navigate,
    };
});

describe("HighRiskFileRowTests", () => {
    // Clear the mock navigate before each test
    beforeEach(() => {
        mock_navigate.mockClear();
    })

    // Clean up after each test
    afterEach(() => {
        cleanup();
    });


    test("rendersFileRiskRowDetailsCorrectly", () => {
        // Create test file
        const test_file = {
            file_id: 1,
            file_name: "Financial_Report_Q4_2025_CONFIDENTIAL.xlsx",
            employees_with_access_count: 5,
            valid_access_count: 1,
            invalid_access_count: 4,
            valid_access_percentage: 20,
            invalid_access_percentage: 80,
            detection_count: 187,
            risk_score: 92.35,
        };

        // Render the high risk file row
        render(
            <MemoryRouter>
                <HighRiskFileRow file={test_file} />
            </MemoryRouter>
        );

        // Ensure all the file's information is correctly rendered on the page
        expect(screen.getByText("Financial_Report_Q4_2025_CONFIDENTIAL.xlsx")).toBeInTheDocument();
        expect(screen.getByText("5")).toBeInTheDocument();
        expect(screen.getByText("20%")).toBeInTheDocument();
        expect(screen.getByText("1 valid, 4 invalid")).toBeInTheDocument();
        expect(screen.getByText("187 detections")).toBeInTheDocument();
        expect(screen.getByRole("button", { name: /more details/i })).toBeInTheDocument();
    });


    test("navigatesToFileOverviewPageWhenMoreDetailsClicked", () => {
        // Create test file
        const test_file = {
            file_id: 42,
            file_name: "contract.pdf",
            employees_with_access_count: 2,
            valid_access_count: 1,
            invalid_access_count: 1,
            valid_access_percentage: 50,
            invalid_access_percentage: 50,
            detection_count: 8,
            risk_score: 54,
        };

        // Render the high risk file row
        render(
            <MemoryRouter>
                <HighRiskFileRow file={test_file} />
            </MemoryRouter>
        );

        fireEvent.click(screen.getByTestId("more-details-button"));

        // Expect navigate to have called /files/42 endpoint (the file's overview page)
        expect(mock_navigate).toHaveBeenCalledWith("/files/42");
    });


    test("rendersHighRiskBadgeWhenInvalidAccessPercentageIs50orMore", () => {
        // Create test file
        const test_file = {
            file_id: 1,
            file_name: "contract.pdf",
            employees_with_access_count: 4,
            valid_access_count: 1,
            invalid_access_count: 3,
            valid_access_percentage: 25,
            invalid_access_percentage: 75,
            detection_count: 10,
            risk_score: 80,
        };

        // Render high risk file
        const { container } = render(
            <MemoryRouter>
                <HighRiskFileRow file={test_file} />
            </MemoryRouter>
        );

        // Ensure the risk badge is 'high' (because invalid access percentage is 75 which is more than 50)
        const riskBadge = container.querySelector('[class*="risk_badge"]');
        expect(riskBadge.className).toMatch(/high/);
    });

})