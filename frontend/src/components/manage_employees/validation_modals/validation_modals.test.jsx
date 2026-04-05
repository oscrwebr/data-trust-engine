import { afterEach, describe, expect, test, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import EmployeeRemoveModal from "./EmployeeRemoveModal"
import PendingAcceptModal from "./PendingAcceptModal"
import PendingRejectModal from "./PendingRejectModal"

describe("Pending Employee Components", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Check that all elements for employee remove modal load as expected", async() => {

        render(
            <MemoryRouter>
                <EmployeeRemoveModal firstname="Test" surname="Case" visible={true}/>
            </MemoryRouter>
        );

        expect(await screen.findByText(/Are you sure you want to remove/)).toBeInTheDocument();
        expect(await screen.findByText(/Test/)).toBeInTheDocument();
        expect(await screen.findByText(/Case/)).toBeInTheDocument();
        expect(await screen.findByText(/from your workspace?/)).toBeInTheDocument();
        expect(await screen.findByText("Yes, remove employee")).toBeInTheDocument();
        expect(await screen.findByText("Cancel")).toBeInTheDocument();
    })

    // Test 2
    test("Check that all elements for pending user accept modal load as expected", async() => {

        render(
            <MemoryRouter>
                <PendingAcceptModal email="test@email.com" visible={true} date={new Date("2026-11-17T14:38:52")}/>
            </MemoryRouter>
        );

        expect(await screen.findByText(/An email containing an invite request will be sent to/)).toBeInTheDocument();
        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        expect(await screen.findByText(/. It will expiry on the/)).toBeInTheDocument();
        expect(await screen.findByText(/17 November 2026/)).toBeInTheDocument();
        expect(await screen.findByText("Yes, accept employee")).toBeInTheDocument();
        expect(await screen.findByText("Cancel")).toBeInTheDocument();
    })

    // Test 3
    test("Check that all elements for pending user reject modal load as expected", async() => {

        render(
            <MemoryRouter>
                <PendingRejectModal email="test@email.com" visible={true}/>
            </MemoryRouter>
        );

        expect(await screen.findByText(/Are you sure you want to reject/)).toBeInTheDocument();
        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        expect(await screen.findByText(/from joining your workspace?/)).toBeInTheDocument();
        expect(await screen.findByText("Yes, reject employee")).toBeInTheDocument();
        expect(await screen.findByText("Cancel")).toBeInTheDocument();
    })

})