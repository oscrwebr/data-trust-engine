import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import DeleteModal from "./DeleteModal"

describe("Delete Role Modal Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });


    // Test 1
    test("Test all content in component loads correctly", async () => {
        render(
            <MemoryRouter>
                <DeleteModal visible={true}/>
            </MemoryRouter>
        );

        expect(await screen.findByText(/Are you sure you want to delete this role?/i)).toBeInTheDocument();
        expect(await screen.findByText("Yes, delete role")).toBeInTheDocument();
        expect(await screen.findByText("Cancel")).toBeInTheDocument();
    });
});