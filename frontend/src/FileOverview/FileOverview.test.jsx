import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import FileOverviewPage from "./FileOverviewPage";

// Mocking components used on page to focus tests on FileOverviewPage logic
vi.mock("./FileScanHistoryItem", () => ({
    default: ({ scan }) => <div>Scan History Item: {scan.scan_id}</div>
}));

vi.mock("./LatestScanResultCard", () => ({
    default: ({ result }) => (
        <div>
            Latest Result Card: {result.subcategory ?? result.sensitivity_subcategory ?? "Unknown"}
        </div>
    )
}));


// Method to render FileOverviewPage with router context
function renderComponent() {
    return render(
        <MemoryRouter initialEntries={["/files/1"]}>
            <Routes>
                <Route path="/files/:file_id" element={<FileOverviewPage />} />
            </Routes>
        </MemoryRouter>
    );
}


describe("FileOverviewPageTests", () => {
    // Reset mocks before each test
    beforeEach(() => {
        vi.restoreAllMocks();
    });


    // Clear mock calls after each test
    afterEach(() => {
        cleanup();
        vi.clearAllMocks();
    });


    // Test to ensure the page shows that the page is loading initially upon open
    test("fileOverviewPageShowsLoadingStateInitially", () => {
        vi.spyOn(global, "fetch").mockImplementation(() => new Promise(() => {}));

        renderComponent();

        // Expect the loading text to be visible
        expect(screen.getByText("File loading...")).toBeInTheDocument();
    });


    // Test to ensure page fetches data and renders everything correctly
    test("fileOverviewPageFetchesFileDataAndRenders", async () => {

        // Mock backend responses
        const mockFile = {
            file_id: 1,
            file_name: "contract.pdf",
            hash: "abc123"
        };

        const mockScanHistory = [
            { scan_id: 101 },
            { scan_id: 102 }
        ];

        const mockLatestScanResults = [
            { category: "Personal", subcategory: "NAME" },
            { category: "Personal", subcategory: "EMAIL" },
            { category: "Financial", subcategory: "IBAN" }
        ];

        // Mock fetch calls
        vi.spyOn(global, "fetch")
            .mockResolvedValueOnce({
                json: async () => mockFile
            })
            .mockResolvedValueOnce({
                json: async () => mockScanHistory
            })
            .mockResolvedValueOnce({
                json: async () => mockLatestScanResults
            });

        renderComponent();

        // Wait for async rendering to complete
        await waitFor(() => {
            expect(screen.getByText("contract.pdf")).toBeInTheDocument();
        });

        // Ensure file information is rendered
        expect(screen.getByText("abc123")).toBeInTheDocument();

        // Ensure section titles are rendered
        expect(screen.getByText("Latest Scan Results")).toBeInTheDocument();
        expect(screen.getByText("Scan History")).toBeInTheDocument();

        // Ensure grouping labels are rendered
        expect(screen.getByText("Personal")).toBeInTheDocument();
        expect(screen.getByText("Financial")).toBeInTheDocument();

        // Ensure results are rendered 
        expect(screen.getByText("Latest Result Card: NAME")).toBeInTheDocument();
        expect(screen.getByText("Latest Result Card: EMAIL")).toBeInTheDocument();
        expect(screen.getByText("Latest Result Card: IBAN")).toBeInTheDocument();

        // Ensure scan history rendered
        expect(screen.getByText("Scan History Item: 101")).toBeInTheDocument();
        expect(screen.getByText("Scan History Item: 102")).toBeInTheDocument();

        // Ensure correct API calls were made
        expect(global.fetch).toHaveBeenCalledTimes(4);
        expect(global.fetch).toHaveBeenNthCalledWith(
            1,
            "http://localhost:8000/scanning/get_file/1"
        );
        expect(global.fetch).toHaveBeenNthCalledWith(
            2,
            "http://localhost:8000/scanning/get_file_scans/1"
        );
        expect(global.fetch).toHaveBeenNthCalledWith(
            3,
            "http://localhost:8000/scanning/get_file_latest_scan_results/1"
        );
    })


    // Test to ensure page shows 'File not found' when file is null"
    test("fileOverviewPageShowsFileNotFound", async () => {
        // Mock API calls returning null file
        vi.spyOn(global, "fetch")
            .mockResolvedValueOnce({
                json: async () => null
            })
            .mockResolvedValueOnce({
                json: async () => []
            })
            .mockResolvedValueOnce({
                json: async () => []
            });

        renderComponent();

        // Expect file not found text after waiting for UI update
        await waitFor(() => {
            expect(screen.getByText("File not found.")).toBeInTheDocument();
        });
    })


    // Test to ensure empty scan results and empty file history is rendered appropriately
    test("fileOverviewPageRendersEmptyScanResultsAndScanHistory", async () => {
        // Mock a file
        const mockFile = {
            file_id: 1,
            file_name: "empty_file.pdf",
            hash: "emptyhash123"
        };

        // Mock API calls returning empty file
        vi.spyOn(global, "fetch")
            .mockResolvedValueOnce({
                json: async () => mockFile
            })
            .mockResolvedValueOnce({
                json: async () => []
            })
            .mockResolvedValueOnce({
                json: async () => []
            });

        renderComponent();

        // Ensure file name still exists
        await waitFor(() => {
            expect(screen.getByText("empty_file.pdf")).toBeInTheDocument();
        });

        // Ensure section titles still exist
        expect(screen.getByText("Latest Scan Results")).toBeInTheDocument();
        expect(screen.getByText("Scan History")).toBeInTheDocument();

        // Ensure no items are rendered as file is empty
        expect(screen.queryByText(/Latest Result Card:/)).not.toBeInTheDocument();
        expect(screen.queryByText(/Scan History Item:/)).not.toBeInTheDocument();
    })
})