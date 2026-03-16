import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import Dashboard from "./Dashboard.jsx";

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

import api from "../api/axiosConfig.js";
describe("Dashboard Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Test modal box appears when invite employee button clicked", async () => {
        render(
            <MemoryRouter>
                <Dashboard/>
            </MemoryRouter>
        );

        const invite_button = screen.getByText("Invite Employee");
        fireEvent.click(invite_button);
        expect(screen.getByRole("dialog")).toBeInTheDocument();
    })
})