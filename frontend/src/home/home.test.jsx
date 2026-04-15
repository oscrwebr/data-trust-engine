import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import Home from "./home.jsx"

vi.mock("../api/axiosConfig.js", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: [] }),
    post: vi.fn().mockResolvedValue({ data: { success: true } }), 
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  },
}));

const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

import api from "../api/axiosConfig.js";
describe("Home Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Test that all major components of the home screen load correctly", async () => {
      render(
            <MemoryRouter>
                <Home/>
            </MemoryRouter>
        );

        expect(await screen.findByText("The Data Trust Engine")).toBeInTheDocument();
        expect(await screen.findByText("Building Trust in Every Data Interaction")).toBeInTheDocument();
        expect(await screen.findByText("Enable secure collaboration and controlled access between organizations. Create trusted data environments where teams can work together with confidence.")).toBeInTheDocument();
        expect(await screen.findByText("Secure")).toBeInTheDocument();
        expect(await screen.findByText("Scalable")).toBeInTheDocument();
        expect(await screen.findByText("Compliant")).toBeInTheDocument();
        expect(await screen.findByText("Automated Classification System")).toBeInTheDocument();
        expect(await screen.findByText("Security Noise Filter")).toBeInTheDocument();
        expect(await screen.findByText("Universal Trust Score")).toBeInTheDocument();
    })


    // Test 2
    test("Test that when create workspace is clicked, user is redirected to correct window location", async () => {
        const originalLocation = window.location;
        delete window.location;
        window.location = { href: "" };

        render(
            <MemoryRouter>
                <Home/>
            </MemoryRouter>
        );

        expect(await screen.findByText("Create a Workspace")).toBeInTheDocument();
        const button = screen.getByText("Create a Workspace");
        fireEvent.click(button);
        
        expect(window.location.href).toBe(
            "http://localhost:8000/auth/sign-in?next=/create-workspace&signup=true&role=1"
        );
        window.location = originalLocation

    })


    // Test 3
    test("Test that when get started is clicked, user is redirected to correct window location", async () => {
        const originalLocation = window.location;
        delete window.location;
        window.location = { href: "" };

        render(
            <MemoryRouter>
                <Home/>
            </MemoryRouter>
        );

        expect(await screen.findByText("Get Started")).toBeInTheDocument();
        const button = screen.getByText("Get Started");
        fireEvent.click(button);
        
        expect(window.location.href).toBe(
            "http://localhost:8000/auth/sign-in?next=/dashboard&signup=true&role=2"
        );
        window.location = originalLocation

    })


    // Test 4
    test("Test that sign-in button is on home screen and that when clicked, correct navigate is called", async () => {
        render(
            <MemoryRouter>
                <Home/>
            </MemoryRouter>
        );

        expect(await screen.findByText("Sign in")).toBeInTheDocument();
        const button = screen.getByText("Sign in");
        fireEvent.click(button);
        
        expect(mockNavigate).toHaveBeenCalledWith("/dashboard");
    })
})
