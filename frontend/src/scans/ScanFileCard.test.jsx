import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import userEvent from "@testing-library/user-event";
import ScanFileCard from "./ScanFileCard";

const mockNavigate = vi.fn();

vi.mock("react-router-dom", () => ({
    useNavigate: () => mockNavigate
}));

vi.mock("./utils/formatNamingConventionName", () => ({
    formatNamingConventionName: vi.fn((value) => value)
}));

// Mock the function that formats the details for a test later on
vi.mock("./utils/formatSubcategoryText", () => ({
    formatSubcategoryText: vi.fn((value) => {
        if (value === "NAME") return "Contains names";
        if (value === "IBAN") return "Contains bank account information";
        return value;
    })
}));

const issueOrganisationScanFile = {
    scan_file_id: 1,
    file_id: 101,
    file_name: "failed file",
    naming_convention_scan_results: [{
        naming_convention_name: "camel_case",
        passed: false,
        suggested_name: "failedFile"
        }
    ]
};

const passedOrganisationScanFile = {
    scan_file_id: 2,
    file_id: 102,
    file_name: "passedFile",
    naming_convention_scan_results: [{
        naming_convention_name: "camel_case",
        passed: true,
        suggested_name: null
        }
    ]
};

const issueSensitivityScanFile = {
    scan_file_id: 3,
    file_id: 103,
    file_name: "sensitive_file",
    sensitivity_scan_results: [
        { category: "Personal", subcategory_name: "NAME" },
        { category: "Financial", subcategory_name: "IBAN" }
    ]
};

describe("ScanFileCardTests", () => {

    beforeEach(() => {
        vi.clearAllMocks();
    });

    afterEach(() => {
        cleanup();
    });

    test("clickingOnScanFileCardNavigatesToCorrectFilePage", async () => {
        render(<ScanFileCard scan_file={issueOrganisationScanFile} scan_type="organisation"/>);
        await userEvent.click(screen.getByText("failed file"));

        expect(mockNavigate).toHaveBeenCalledWith("/files/101");
    });

    test("clickingOnAdvancedDetailsButtonNavigatesToCorrectScanFilePage", async () => {
        render(<ScanFileCard scan_file={issueSensitivityScanFile} scan_type="sensitivity"/>);
        await userEvent.click(screen.getByText("View Advanced Details"));

        expect(mockNavigate).toHaveBeenCalledWith("/scan_file/3");
    });

    test("organisationalScanFileCardShowsDetailsIfIssue", () => {
        render(<ScanFileCard scan_file={issueOrganisationScanFile} scan_type="organisation"/>);

        expect(screen.getByText("Naming Issue")).toBeInTheDocument();
        expect(screen.getByText("failed file")).toBeInTheDocument();

        // Check suggested name is shown
        expect(screen.getByText("failedFile")).toBeInTheDocument();

        const card = screen.getByText("failed file").closest(".scan-page-file-card");
        expect(card).toHaveClass("card-issue");
    });

    test("cleanOrganisationalScanFileCardShowsClean", () => {
        render(<ScanFileCard scan_file={passedOrganisationScanFile} scan_type="organisation"/>);

        expect(screen.getByText("Clean")).toBeInTheDocument();
        expect(screen.getByText("passedFile")).toBeInTheDocument();

        const card = screen.getByText("passedFile").closest(".scan-page-file-card");
        expect(card).toHaveClass("card-clean");
    });

    test("issueSensitivityScanFileCardShowsSimpleDetailsOfDetections", () => {
        render(<ScanFileCard scan_file={issueSensitivityScanFile} scan_type="sensitivity"/>);

        expect(screen.getByText("Detections:")).toBeInTheDocument();
        expect(screen.getByText("Personal")).toBeInTheDocument();
        expect(screen.getByText("Financial")).toBeInTheDocument();
        expect(screen.getByText("Contains names")).toBeInTheDocument();
        expect(screen.getByText("Contains bank account information")).toBeInTheDocument();
    });

});