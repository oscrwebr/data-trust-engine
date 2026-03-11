import {cleanup, render, screen} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Navbar from "./Navbar";
import { test, expect, afterEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import App from "../../App";

afterEach(() => {
    // Clear the DOM after each test to prevent interference between tests
    cleanup();
});

test('renders the navbar component', () => {
    // Arrange
    
    render(<MemoryRouter><Navbar/></MemoryRouter>);

    // Assert
    expect(screen.getByAltText("CIH Logo")).toBeInTheDocument();
    expect(screen.getByText("Files")).toBeInTheDocument();
    expect(screen.getByText("Scans")).toBeInTheDocument();

})

test('navbar renders on all pages', () => {
    // Arrange
    render(<App/>);

    // Assert
    expect(screen.getByAltText("CIH Logo")).toBeInTheDocument();
    expect(screen.getByText("Files")).toBeInTheDocument();
    expect(screen.getByText("Scans")).toBeInTheDocument();
})

test('files item redirects to files page', async () => {
    // Arrange
    render(<MemoryRouter><Navbar/></MemoryRouter>);

    // Act
    await userEvent.click(screen.getByText("Files"));

    // Assert
    expect(screen.getByRole("link", { name: "Files" })).toHaveAttribute("href", "/files");
})

test('scans item redirects to scans page', async () => {
    // Arrange
    render(<MemoryRouter><Navbar/></MemoryRouter>);

    // Act
    await userEvent.click(screen.getByText("Scans"));

    // Assert
    expect(screen.getByRole("link", { name: "Scans" })).toHaveAttribute("href", "/scans");
})