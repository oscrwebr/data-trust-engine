import "@testing-library/jest-dom/vitest";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi, beforeEach, afterEach, describe, test, expect } from "vitest";

import HighRiskFilesDashboard from "./HighRiskFilesDashboard";

// Mock the row component so  tests only focus on the dashboard page logic
vi.mock("./HighRiskFileRow", () => ({
    default: ({ file }) => (
        <div data-testid="high-risk-file-row">
            <span>{file.file_name}</span>
        </div>
    ),
}));

describe("HighRiskFilesDashboard", () => {
    // Reset mocks before each test so tests dont affect eachother
    beforeEach(() => {
        vi.restoreAllMocks();
    });

    // Clean up the rendered DOM after each test
    afterEach(() => {
        cleanup();
    });


    test("showsLoadingStateInitially", () => {
        // Mock fetch with a promise that never resolves so component stays in loading state
        vi.spyOn(global, "fetch").mockImplementation(() => new Promise(() => {}));

        render(
            <MemoryRouter>
                <HighRiskFilesDashboard />
            </MemoryRouter>
        );

        expect(screen.getByText(/high risk files loading/i)).toBeInTheDocument();
    });


    test("fetchesHighRiskFilesAndRendersDashboardContent", async () => {
        // Mock successful backend response with 2 files
        vi.spyOn(global, "fetch").mockResolvedValue({
            ok: true,
            json: async () => ({
                items: [
                    {
                        file_id: 1,
                        file_name: "contract.pdf",
                        employees_with_access_count: 4,
                        valid_access_count: 1,
                        invalid_access_count: 3,
                        valid_access_percentage: 25,
                        invalid_access_percentage: 75,
                        detection_count: 18,
                        risk_score: 88,
                    },
                    {
                        file_id: 2,
                        file_name: "payroll.xlsx",
                        employees_with_access_count: 2,
                        valid_access_count: 1,
                        invalid_access_count: 1,
                        valid_access_percentage: 50,
                        invalid_access_percentage: 50,
                        detection_count: 7,
                        risk_score: 61,
                    },
                ],
                total: 12,
                limit: 10,
                offset: 0,
            }),
        });

        render(
            <MemoryRouter>
                <HighRiskFilesDashboard />
            </MemoryRouter>
        );

        // Wait for async fetch/render to complete
        await waitFor(() => {
            expect(screen.getByText("High-Risk Files Dashboard")).toBeInTheDocument();
        });

        // Check main page content
        expect(
            screen.getByText(/ranked by access risk and sensitivity detections/i)
        ).toBeInTheDocument();

        // Check column headings
        expect(screen.getByText("Risk")).toBeInTheDocument();
        expect(screen.getByText("File Name")).toBeInTheDocument();
        expect(screen.getByText("Employees with Access")).toBeInTheDocument();
        expect(screen.getByText("Valid Access")).toBeInTheDocument();
        expect(screen.getByText("Detections")).toBeInTheDocument();

        // Check that mocked row component rendered both files
        expect(screen.getByText("contract.pdf")).toBeInTheDocument();
        expect(screen.getByText("payroll.xlsx")).toBeInTheDocument();
        expect(screen.getAllByTestId("high-risk-file-row")).toHaveLength(2);
    });


    test("showsErrorStateWhenFetchFails", async () => {
        // Mock failed fetch request
        vi.spyOn(global, "fetch").mockRejectedValue(new Error("Fetch failed"));

        render(
            <MemoryRouter>
                <HighRiskFilesDashboard />
            </MemoryRouter>
        );

        // Ensure error message appears
        await waitFor(() => {
            expect(screen.getByText(/failed to load high risk files/i)).toBeInTheDocument();
        });
    });


    test("showsEmptyStateWhenNoFilesReturned", async () => {
        // Mock successful response with no file rows
        vi.spyOn(global, "fetch").mockResolvedValue({
            ok: true,
            json: async () => ({
                items: [],
                total: 0,
                limit: 10,
                offset: 0,
            }),
        });

        render(
            <MemoryRouter>
                <HighRiskFilesDashboard />
            </MemoryRouter>
        );

        // Ensure 'no high-risk files found' text appears
        await waitFor(() => {
            expect(screen.getByText(/no high-risk files found/i)).toBeInTheDocument();
        });
    });


    test("goesToNextPageWhenNextButtonClicked", async () => {
        // First fetch call = page 1
        // Second fetch call = page 2
        const fetchSpy = vi.spyOn(global, "fetch")
            .mockResolvedValueOnce({
                ok: true,
                json: async () => ({
                    items: [
                        {
                            file_id: 1,
                            file_name: "contract.pdf",
                            employees_with_access_count: 4,
                            valid_access_count: 1,
                            invalid_access_count: 3,
                            valid_access_percentage: 25,
                            invalid_access_percentage: 75,
                            detection_count: 18,
                            risk_score: 88,
                        },
                    ],
                    total: 20,
                    limit: 10,
                    offset: 0,
                }),
            })
            .mockResolvedValueOnce({
                ok: true,
                json: async () => ({
                    items: [
                        {
                            file_id: 2,
                            file_name: "payroll.xlsx",
                            employees_with_access_count: 2,
                            valid_access_count: 1,
                            invalid_access_count: 1,
                            valid_access_percentage: 50,
                            invalid_access_percentage: 50,
                            detection_count: 7,
                            risk_score: 61,
                        },
                    ],
                    total: 20,
                    limit: 10,
                    offset: 10,
                }),
            });

        render(
            <MemoryRouter>
                <HighRiskFilesDashboard />
            </MemoryRouter>
        );

        // Wait for page 1 data
        await waitFor(() => {
            expect(screen.getByText("contract.pdf")).toBeInTheDocument();
        });

        // Move to next page
        fireEvent.click(screen.getByRole("button", { name: /next/i }));

        // Wait for page 2 data
        await waitFor(() => {
            expect(screen.getByText("payroll.xlsx")).toBeInTheDocument();
        });

        // Ensure the second fetch used the correct offset
        expect(fetchSpy).toHaveBeenNthCalledWith(
            2,
            expect.stringContaining("limit=10&offset=10")
        );
    });


    test("disablesPreviousButtonOnFirstPage", async () => {
        // Mock empty first page response
        vi.spyOn(global, "fetch").mockResolvedValue({
            ok: true,
            json: async () => ({
                items: [],
                total: 0,
                limit: 10,
                offset: 0,
            }),
        });

        render(
            <MemoryRouter>
                <HighRiskFilesDashboard />
            </MemoryRouter>
        );

        await waitFor(() => {
            expect(screen.getByRole("button", { name: /previous/i })).toBeDisabled();
        });
    });
});