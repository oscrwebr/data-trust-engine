import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import RoleCard from "./RoleCard";

describe("Role Card Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });


    // Test 1
    test("Test all content in component loads correctly", async () => {
        render(
            <MemoryRouter>
                <RoleCard name="Test Role" last_updated="2026-04-17T17:44:04"/>
            </MemoryRouter>
        );

        expect(await screen.findByText(/Test Role/i)).toBeInTheDocument();
        expect(await screen.findByText(/17 April 2026 at 17:44:04/i)).toBeInTheDocument();
        expect(await screen.findByTestId("edit-button")).toBeInTheDocument();
        expect(await screen.findByTestId("delete-button")).toBeInTheDocument();
    });
});