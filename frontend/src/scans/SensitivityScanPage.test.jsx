import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import SensitivityScanPage from "./SensitivityScanPage";

// Mock the scan file cards used on each scan type page
vi.mock("./ScanFileCard", () => ({
    default: ({ scan_file }) => (
        <div>ScanFileCard - {scan_file.file_name}</div>
    )
}));

// The scan type pages need to take in a scan so this is a mocked scan that is used for these tests
// Same as OrganisationScanPage, this mock data was generated using the AI Tool 'ChatGPT' (fed the structure of the backend response and asked to generate mock data)
export const mockScan = {
    scan_id: 1,
    scan_type: "sensitivity",
    file_count: 5,
    detection_counts: {
        personal: 201,
        financial: 250,
        legal_case: 2
    },
    files: [
        {
            scan_file_id: 1,
            file_id: 201,
            file_name: "employee_records.xlsx",
            sensitivity_scan_results: [
                { category: "personal", subcategory_name: "NAME" },
                { category: "personal", subcategory_name: "EMAIL" }
            ]
        },
        {
            scan_file_id: 2,
            file_id: 202,
            file_name: "bank_transactions.csv",
            sensitivity_scan_results: [
                { category: "financial", subcategory_name: "IBAN" },
                { category: "financial", subcategory_name: "CARD_NUMBER" }
            ]
        },
        {
            scan_file_id: 3,
            file_id: 203,
            file_name: "legal_documents.pdf",
            sensitivity_scan_results: [
                { category: "legal_case", subcategory_name: "CASE_ID" }
            ]
        }
    ]
};

function renderSensitivityScanPage() {
    return render(
        <MemoryRouter>
            <SensitivityScanPage scan={mockScan} />
        </MemoryRouter>
    );
}

describe("SensitivityScanPageTests", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    afterEach(() => {
        cleanup();

    }); 

    // Total Files + Detection count tests
    test("sensitivityScanPageShowsCorrectTotalFilesScanned", () => {
        renderSensitivityScanPage();

        expect(screen.getByText("Total Files")).toBeInTheDocument();
        expect(screen.getByText("5")).toBeInTheDocument();
    });

    test("sensitivityScanPageShowsCorrectPIIDetections", () => {
        renderSensitivityScanPage();

        expect(screen.getByText("PII")).toBeInTheDocument();
        expect(screen.getByText("201")).toBeInTheDocument();
    });

    test("sensitivityScanPageShowsCorrectFinancialDetections", () => {
        renderSensitivityScanPage();

        expect(screen.getByText("Financial")).toBeInTheDocument();
        expect(screen.getByText("250")).toBeInTheDocument();
    });

    test("sensitivityScanPageShowsCorrectLegalDetections", () => {
        renderSensitivityScanPage();

        expect(screen.getByText("Legal")).toBeInTheDocument();
        expect(screen.getByText("2")).toBeInTheDocument();
    });

    // Card class tests
    test("sensitivityScanPageCorrectlyAppliesCardClass", () => {
        renderSensitivityScanPage();

        const piiCard = screen.getByText("PII").closest(".scan-page-card");
        const financialCard = screen.getByText("Financial").closest(".scan-page-card");
        const legalCard = screen.getByText("Legal").closest(".scan-page-card");

        // Each card has a threshold of 50 detections per file scanned before it becomes 'critical'
        // Financial should be critical as it has 250 detections across 5 files
        expect(piiCard).toHaveClass("issues");
        expect(financialCard).toHaveClass("critical");
        expect(legalCard).toHaveClass("issues");


    });



});