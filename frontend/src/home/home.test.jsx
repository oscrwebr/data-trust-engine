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
describe("Invite Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Test that signup button is on home screen and that when clicked, correct navigate is called", async () => {
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

        expect(await screen.findByText("Create a workspace")).toBeInTheDocument();
        const button = screen.getByText("Create a workspace");
        fireEvent.click(button);
        
        expect(window.location.href).toBe(
            "http://localhost:8000/auth/sign-in?next=/create-workspace&signup=true"
        );
        window.location = originalLocation

    })

})
