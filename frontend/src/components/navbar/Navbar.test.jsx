// import {cleanup, render, screen} from "@testing-library/react";
// import userEvent from "@testing-library/user-event";
// import Navbar from "./Navbar";
// import { test, expect, afterEach } from "vitest";
// import { MemoryRouter } from "react-router-dom";
// import App from "../../App";

// afterEach(() => {
//     // Clear the DOM after each test to prevent interference between tests
//     cleanup();
// });

// test('navbar renders on dashboard page', () => {
//     // Arrange
//     render(<MemoryRouter initialEntries={["/dashboard"]}><App/></MemoryRouter>);

//     // Assert
//     expect(screen.getByAltText("CIH Logo")).toBeInTheDocument();
//     expect(screen.getByText("Files")).toBeInTheDocument();
//     expect(screen.getByText("Scans")).toBeInTheDocument();
// })

// test('navbar does not render on home page', () => {
//     // Arrange
//     render(<MemoryRouter initialEntries={["/"]}><App /></MemoryRouter>);

//     // Assert
//     expect(screen.queryByText("Files")).not.toBeInTheDocument();
// });


// test('files item redirects to files page', async () => {
//     // Arrange
//     render(<MemoryRouter><Navbar/></MemoryRouter>);

//     // Act
//     await userEvent.click(screen.getByText("Files"));

//     // Assert
//     expect(screen.getByRole("link", { name: "Files" })).toHaveAttribute("href", "/files");
// })

// test('scans item redirects to scans page', async () => {
//     // Arrange
//     render(<MemoryRouter><Navbar/></MemoryRouter>);

//     // Act
//     await userEvent.click(screen.getByText("Scans"));

//     // Assert
//     expect(screen.getByRole("link", { name: "Scans" })).toHaveAttribute("href", "/scans");
// })