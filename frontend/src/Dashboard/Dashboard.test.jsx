import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, test, vi } from "vitest";
import Dashboard from "../Dashboard/Dashboard.jsx";

vi.mock("axios");
describe("Dashboard Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

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