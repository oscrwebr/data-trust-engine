import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import api from "../api/axiosConfig";
import ScanPage from "./ScanPage";


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
        vi.restoreAllMocks();
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    // Test that the page shows a loading message while loading the scan page (not just a blank page)
    test("scanPageShowsLoadingStateInitially", () => {
        vi.spyOn(global, "fetch").mockImplementation(() => new Promise(() => {})); 
        renderScanPage();
        expect(screen.getByText("Loading scan...")).toBeInTheDocument();
    });

});

