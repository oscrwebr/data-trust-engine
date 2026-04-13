import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import OrganisationScanPage from "./OrganisationScanPage";

// Mock the scan file cards used on each scan type page
vi.mock("./ScanFileCard", () => ({
    default: ({ scan_file }) => (
        <div>ScanFileCard - {scan_file.file_name}</div>
    )
}));

// The scan type pages need to take in a scan so this is a mocked scan that is used for these tests
// This mock data was generated using the AI Tool 'ChatGPT' (fed the structure of the backend response and asked to generate mock data)
const mockScan = {
    scan_id: 1,
    scan_type: "organisation",
    file_count: 3,
    files: [
        {
            scan_file_id: 1,
            file_id: 101,
            file_name: "annual_report_file",
            naming_convention_scan_results: [
                {
                    naming_convention_name: "camel_case",
                    passed: false,
                    suggested_name: "annualReportFile"
                },
                {
                    naming_convention_name: "snake_case",
                    passed: true,
                    suggested_name: null
                }
            ]
        },
        {
            scan_file_id: 2,
            file_id: 102,
            file_name: "bad file name",
            naming_convention_scan_results: [
                {
                    naming_convention_name: "camel_case",
                    passed: false,
                    suggested_name: "badFileName"
                },
                {
                    naming_convention_name: "snake_case",
                    passed: false,
                    suggested_name: "bad_file_name"
                }
            ]
        },
        {
            scan_file_id: 3,
            file_id: 103,
            file_name: "another bad file",
            naming_convention_scan_results: [
                {
                    naming_convention_name: "camel_case",
                    passed: false,
                    suggested_name: "anotherBadFile"
                },
                {
                    naming_convention_name: "snake_case",
                    passed: false,
                    suggested_name: "another_bad_file"
                }
            ]
        }
    ]
};

function renderOrganisationScanPage() {
    return render(<OrganisationScanPage scan={mockScan} />);
}

describe("OrganisationScanPageTests", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    afterEach(() => {
        cleanup();
    });

    test("organisationScanPageShowsCorrectTotalFilesScanned", async () => {
        renderOrganisationScanPage();
        expect(screen.getByText("Total Files Scanned")).toBeInTheDocument();
        expect(screen.getByText("3")).toBeInTheDocument();
    });

    test("organisationScanPageShowsCorrectNamingIssuesCount", () => {
        renderOrganisationScanPage();

        expect(screen.getByText("Naming Issues")).toBeInTheDocument();
        expect(screen.getByText("2")).toBeInTheDocument();
    });

    // Testing the helper function that calculates clean file percentage
    // (In the mock data there are 3 files but only one passes)
    test("organisationScanPageShowsCorrectCleanFilesPercentage", () => {
        renderOrganisationScanPage();

        expect(screen.getByText("Clean Files")).toBeInTheDocument();
        expect(screen.getByText("33%")).toBeInTheDocument();
    });

    // Test that the Clean Files card has the correct class applied using the helper function 'getCleanFilesClass'
    // As said above, the mock data has 33% clean files which should apply the critical class (below 50%)
    test("organisationScanPageAppliesCorrectClassToCleanFilesCard", () => {
        renderOrganisationScanPage();
        const cleanFilesCard = screen.getByText("Clean Files").closest(".scan-page-card");

        expect(cleanFilesCard).toHaveClass("critical");
    });

    // Test that the Naming Issues card has the correct class applied using the helper function 'getScanPageCardClass'
    // The mock data has 66% of files with naming issues which should apply the critical class (above 50%)
    test("organisationScanPageAppliesCorrectClassToNamingIssuesCard", () => {
        renderOrganisationScanPage();
        const namingIssuesCard = screen.getByText("Naming Issues").closest(".scan-page-card");

        expect(namingIssuesCard).toHaveClass("critical");
    });

    test("organisationScanPageRendersAScanFileCardForEachFile", () => {
        renderOrganisationScanPage();

        expect(screen.getByText("ScanFileCard - annual_report_file")).toBeInTheDocument();
        expect(screen.getByText("ScanFileCard - bad file name")).toBeInTheDocument();
        expect(screen.getByText("ScanFileCard - another bad file")).toBeInTheDocument();
    });




});