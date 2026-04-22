import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import api from "../api/axiosConfig";
import ScanFile from "./ScanFile";
import userEvent from "@testing-library/user-event";

vi.mock("../api/axiosConfig");

function renderScanFilePage() {
    return render(
        <MemoryRouter initialEntries={["/scan-file/1"]}>
            <Routes>
                <Route path="/scan-file/:scanFileId" element={<ScanFile />} />
            </Routes>
        </MemoryRouter>
    );
}

const mockScanFile = {
    scan_file_id: 1,
    file_id: 1,
    file_name: "test_file.pdf",
    hash: "abc123",
    scan_id: 1,
    started_at: "2024-01-01T12:00:00Z",
    completed_at: "2024-01-01T12:30:00Z",
    total_detections: 10,
    category_counts: {
        "personal": 4,
        "financial": 5,
        "legal_case": 1
    },
    detections: [
        {
            scan_file_detection_id: 1,
            category: "Personal",
            subcategory: "NAME",
            page_number: 1,
        },
        {
            scan_file_detection_id: 2,
            category: "Financial",
            subcategory: "IBAN",
            page_number: 1,
        },
        {
            scan_file_detection_id: 3,
            category: "Legal Case",
            subcategory: "CITATION",
            page_number: 2,
        },
        {
            scan_file_detection_id: 4,
            category: "Personal",
            subcategory: "ADDRESS",
            page_number: 2,
        },
        {
            scan_file_detection_id: 5,
            category: "Financial",
            subcategory: "IBAN",
            page_number: 2,
        },
        {
            scan_file_detection_id: 6,
            category: "Personal",
            subcategory: "NAME",
            page_number: 3,
        },
        {
            scan_file_detection_id: 7,
            category: "Financial",  
            subcategory: "IBAN",
            page_number: 3,
        },
        {
            scan_file_detection_id: 8,
            category: "Financial",
            subcategory: "IBAN",
            page_number: 3,
        },
        {
            scan_file_detection_id: 9,
            category: "Personal",
            subcategory: "EMAIL",
            page_number: 4,
        },
        {
            scan_file_detection_id: 10,
            category: "Financial",
            subcategory: "IBAN",
            page_number: 4,
        }
    ]
}

describe("ScanFileTests", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    afterEach(() => {
        cleanup();
    }); 

    test("scanFilePageShowsLoadingStateWhenLoading", () => {
        api.get.mockReturnValue(new Promise(() => {}));

        renderScanFilePage();

        expect(screen.getByText("Loading scanned file...")).toBeInTheDocument();
    });

    test("scanFilePageShowsErrorMessageIfApiCallFails", async () => {
        api.get.mockRejectedValue(new Error("API error"));
        renderScanFilePage();
        await waitFor(() => expect(screen.getByText("Error loading scanned file.")).toBeInTheDocument());
    });
    
    test("scanFilePageReceivesCorrectDataFromApi", async () => {
        api.get.mockResolvedValue({ data: mockScanFile });

        renderScanFilePage();

        await waitFor(() => {
            expect(api.get).toHaveBeenCalledWith("/scanning/get_scan_file_by_id/1");
        });

    });

    test("scanFilePageDisplaysScanFileDetailsCorrectly", async () => {
    
        api.get.mockResolvedValue({ data: mockScanFile });

    
        renderScanFilePage();

        expect(await screen.findByText("test_file.pdf")).toBeInTheDocument();

        expect(screen.getByText("Scan ID: 1")).toBeInTheDocument();
        expect(screen.getByText("Scan File ID: 1")).toBeInTheDocument();
        expect(screen.getByText("File ID: 1")).toBeInTheDocument();

        expect(screen.getByText("Total Detections")).toBeInTheDocument();
        expect(screen.getByText("10")).toBeInTheDocument();
    });

    test("scanFilePageCorrectlyRendersCategoryCounts", async () => {
        api.get.mockResolvedValue({ data: mockScanFile });

        renderScanFilePage();

        expect(await screen.findByText("PII")).toBeInTheDocument();
        expect(screen.getByText("4")).toBeInTheDocument();

        expect(screen.getByText("Financial")).toBeInTheDocument();
        expect(screen.getByText("5")).toBeInTheDocument();

        expect(screen.getByText("Legal")).toBeInTheDocument();
        expect(screen.getByText("1")).toBeInTheDocument();

        });

    test("scanFilePageRendersCorrectAmountOfPageAccordions", async () => {
        api.get.mockResolvedValue({ data: mockScanFile });

        renderScanFilePage();

        await screen.findByText("test_file.pdf");

        const pages = await screen.findAllByText(/Page \d+/);
        const pageNumbers = new Set(mockScanFile.detections.map(detection => detection.page_number));
        expect(pages).toHaveLength(pageNumbers.size);
    });

    test("pagesRenderInAscendingOrder", async () => {
        api.get.mockResolvedValue({ data: mockScanFile });
        renderScanFilePage();

        
        const pages = await screen.findAllByText(/Page \d+/);
        expect (pages[0]).toHaveTextContent("Page 1");
        expect (pages[1]).toHaveTextContent("Page 2");
        expect (pages[2]).toHaveTextContent("Page 3");
        expect (pages[3]).toHaveTextContent("Page 4");
    });

    test("pagesContainCorrectDetections", async () => {
        api.get.mockResolvedValue({ data: mockScanFile });
        renderScanFilePage();

        const page1 = await screen.findByText("Page 1");
        await userEvent.click(page1);

        // https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector
        const accordion = document.querySelector(".p-accordion-content");

        // https://testing-library.com/docs/dom-testing-library/api-within/
        expect(within(accordion).getByText("NAME")).toBeInTheDocument();
        expect(within(accordion).getByText("IBAN")).toBeInTheDocument();
        expect(within(accordion).getByText("Personal")).toBeInTheDocument();
        expect(within(accordion).getByText("Financial")).toBeInTheDocument();
    });


});