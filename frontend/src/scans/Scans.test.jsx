import { test, expect, afterEach, vi, beforeEach } from "vitest";
import {render, screen} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import App from "../App";
import api from "../api/axiosConfig";
import Scans from "./Scans";


vi.mock("../api/axiosConfig");


const mockScans = [
    { scan_id: 1, scan_type: "organisation", started_at: "2026-03-24T12:00:00", finished_at: "2026-03-24T12:05:00", file_count: 5 },
    { scan_id: 2, scan_type: "sensitivity", started_at: "2026-03-24T13:00:00", finished_at: "2026-03-24T13:10:00", file_count: 10 }
];


afterEach(() => {
  vi.clearAllMocks();
});

// Async to wait for scans to fully load on the page so "Loading..." is not shown
test('scans are correctly rendered when on scans page', async () => {
    // Arrange
    api.get.mockResolvedValue({ data: mockScans });

    // Act
    
    render(<MemoryRouter><Scans/></MemoryRouter>);

    // Assert
    expect(await screen.findByText("Organisational")).toBeInTheDocument();
    expect(await screen.findByText("Sensitivity")).toBeInTheDocument();
    expect(await screen.findByText("12:00:00, 24/03/2026")).toBeInTheDocument();
    expect(await screen.findByText("13:00:00, 24/03/2026")).toBeInTheDocument();
    expect(await screen.findByText("12:05:00, 24/03/2026")).toBeInTheDocument();
    expect(await screen.findByText("13:10:00, 24/03/2026")).toBeInTheDocument();
    expect(await screen.findByText("5")).toBeInTheDocument();
    expect(await screen.findByText("10")).toBeInTheDocument();

})

// All scans should navigate to '/scans/(scan_id)' when clicked 
test('scan card navigates to correct page when clicked', async () => {
    // Arrange
    api.get.mockResolvedValue({ data: mockScans });

    // Act
    render(<MemoryRouter><Scans/></MemoryRouter>);
    await userEvent.click(await screen.findByText("Organisational"));

    // Assert
    // Each ScanCard is wrapped in a <Link> component
    const links = await screen.findAllByRole("link");

    expect(links[0]).toHaveAttribute("href", "/scans/1");
    expect(links[1]).toHaveAttribute("href", "/scans/2");
});

test('displays error message when API call fails', async () => {
    // Arrange
    api.get.mockRejectedValue(new Error("API Error"));

    // Act
    render(<MemoryRouter><Scans/></MemoryRouter>);

    // Assert
    expect(await screen.findByText("Error loading scans.")).toBeInTheDocument();
});