import { afterEach, describe, expect, test, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import PendingEmployeeRow from "./PendingEmployeeRow"
import PendingEmployeeSquare from "./PendingEmployeeSquare"

describe("Pending Employee Components", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Check that all elements for pending employee (type 'request') row card load as expected", async() => {

        render(
            <MemoryRouter>
                <PendingEmployeeRow status="request" email="test@email.com"/>
            </MemoryRouter>
        );

        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        expect(await screen.findByText("Accept")).toBeInTheDocument();
        expect(await screen.findByText("Reject")).toBeInTheDocument();
        expect(await screen.findByText("This employee has requested to join your workspace")).toBeInTheDocument();
    })


    // Test 2
    test("Check that all elements for pending employee (type 'invite') row card load as expected", async() => {

        render(
            <MemoryRouter>
                <PendingEmployeeRow status="invite" email="test@email.com" datetime={new Date("2026-11-17T14:38:52")}/>
            </MemoryRouter>
        );

        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        expect(await screen.findByText("Pending")).toBeInTheDocument();
        expect(await screen.findByText(/An invite was sent on the/)).toBeInTheDocument();
        expect(await screen.findByText(/17 November 2026/)).toBeInTheDocument();
        expect(await screen.findByText(/14:38:52/)).toBeInTheDocument();

    })


    // Test 3
    test("Check that all elements for pending employee (type 'request') square card load as expected", async() => {
        render(
            <MemoryRouter>
                <PendingEmployeeSquare status="request" email="test@email.com"/>
            </MemoryRouter>
        );

        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        expect(await screen.findByText("Accept")).toBeInTheDocument();
        expect(await screen.findByText("Reject")).toBeInTheDocument();
        expect(await screen.findByTestId("request-icon")).toBeInTheDocument();
    })

    
    // Test 4
    test("Check that all elements for pending employee (type 'invite') square card load as expected", async() => {
        render(
            <MemoryRouter>
                <PendingEmployeeSquare status="invite" email="test@email.com" datetime={new Date("2026-11-17T14:38:52")}/>
            </MemoryRouter>
        );

        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        expect(await screen.findByText(/Invite sent on the/)).toBeInTheDocument();
        expect(await screen.findByText(/17 November 2026/)).toBeInTheDocument();
        expect(await screen.findByText(/14:38:52/)).toBeInTheDocument();

        expect(await screen.findByTestId("invite-icon")).toBeInTheDocument();
    })

})