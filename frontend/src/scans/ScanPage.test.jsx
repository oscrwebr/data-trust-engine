import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import api from "../api/axiosConfig";
import ScanPage from "./ScanPage";

vi.mock("../api/axiosConfig");

// Mocking the scan type pages (needed to render ScanPage)
vi.mock("./OrganisationScanPage", () => ({
    default: ({ scan }) => <div>Organisation Scan Page - Scan {scan.scan_id}</div>
}));

vi.mock("./SensitivityScanPage", () => ({
    default: ({ scan }) => <div>Sensitivity Scan Page - Scan {scan.scan_id}</div>
}));

function renderScanPage() {
    return render(
        <MemoryRouter initialEntries={["/scans/1"]}>
            <Routes>
                <Route path="/scans/:scanId" element={<ScanPage />} />
            </Routes>
        </MemoryRouter>
    );
}

describe("ScanPageTests", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    // Test that the page shows a loading message while loading the scan page (not just a blank page)
    test("scanPageShowsLoadingStateWhenLoading", () => {
        api.get.mockReturnValue(new Promise(() => {}));

        renderScanPage();

        expect(screen.getByText("Loading scan...")).toBeInTheDocument();
    });

    // Test that the page shows an error message if the 'api.get' call fails
    test("scanPageShowsErrorMessageIfApiCallFails", async () => {
        api.get.mockRejectedValue(new Error("API error"));
        renderScanPage();
        await waitFor(() => expect(screen.getByText("Error loading scan.")).toBeInTheDocument());
    });

    // Test that the page shows an error message if no scan is returned
    test("scanPageShowsMessageIfNoScanIsFound", async () => {
        api.get.mockResolvedValue({ data: null });
        renderScanPage();
        await waitFor(() => expect(screen.getByText("No scan found.")).toBeInTheDocument());
    });

    // Tests for scan page rendering the correct scan type page
    // (The mocks we created at the start)
    test("scanPageRendersOrganisationScanPageForOrganisationScan", async () => {
        // Mock organisational scan data
        api.get.mockResolvedValue({
            data: {
                scan_id: 1,
                scan_type: "organisation",
                finished_at: "2026-04-06T20:07:27",
                file_count: 5,
                files: []
            }
        });

        renderScanPage();

        // Use the mock that we set at the start to check whether the correct page is rendered
        expect(await screen.findByText("Organisation Scan Page - Scan 1")).toBeInTheDocument();
    });

    test("scanPageRendersSensitivityScanPageForSensitivityScan", async () => {
        // Mock sensitivity scan data
        api.get.mockResolvedValue({
            data: {
                scan_id: 2,
                scan_type: "sensitivity",
                finished_at: "2026-04-06T20:07:27",
                file_count: 5,
                files: []
            }
        });

        renderScanPage();

        // Use the mock that we set at the start to check whether the correct page is rendered
        expect(await screen.findByText("Sensitivity Scan Page - Scan 2")).toBeInTheDocument();
    });

    test("scanPageShowsErrorMessageIfScanTypeIsUnknown", async () => {
        // Mock scan data with unknown scan type
        api.get.mockResolvedValue({
            data: {
                scan_id: 3,
                scan_type: "unknown_type",
                finished_at: "2026-04-06T20:07:27",
                file_count: 5,
                files: []
            }
        });

        renderScanPage();

        // Expect error message about fetching scan type
        expect(await screen.findByText("Error fetching scan type.")).toBeInTheDocument();

    });



});

