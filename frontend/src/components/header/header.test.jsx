import Header from "./header";
import { cleanup, fireEvent, getByTestId, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, test, vi } from "vitest";
import React from "react";
import { Toast } from "primereact/toast";

describe("Header Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("All information is correctly displayed in the header", async() => {
        const toastRef = { current: { show: vi.fn(), clear: vi.fn() } };
        render(
            <Header
                firstname="John"
                lastname="Smith"
                workspace="Test Workspace"
                sidebarVisible={true}
                setSidebarVisible={vi.fn()}
                toastRef={toastRef}
            />
        );

        expect(screen.getByText("John Smith /")).toBeInTheDocument();
        expect(screen.getByText("Test Workspace")).toBeInTheDocument();
        expect(screen.getByTestId("notification-button")).toBeInTheDocument();
    })


    // Test 2
    test("When there are no notifications, the badge number is 0", async() => {
        const toastRef = { current: { show: vi.fn(), clear: vi.fn() } };
        render(
            <Header
                firstname="John"
                lastname="Smith"
                workspace="Test Workspace"
                sidebarVisible={true}
                setSidebarVisible={vi.fn()}
                toastRef={toastRef}
            />
        );

        let badge = screen.getByTestId("badge");
        expect(badge.textContent).toBe(""); 
    })

    // Test 3
    test("When are 2 notifications, the badge number is 2", async() => {
        const toastRef = { current: { show: vi.fn(), clear: vi.fn() } };

        render(
            <Header
                firstname="John"
                lastname="Smith"
                workspace="Test Workspace"
                sidebarVisible={true}
                setSidebarVisible={vi.fn()}
                toastRef={toastRef}
                notifications={[
                    { id: 1, title: "Test", body: "Body", datetime: "2026-03-23T20:53:26" },
                    { id: 2, title: "Test2", body: "Body2", datetime: "2026-03-23T21:00:00" },
                ]}
            />
        );

        const badge = screen.getByTestId("badge");
        expect(badge.textContent).toBe("2");
    })

    // Test 4
    test("When a notification is added and the user clicks on the icon, the notification is displayed", async() => {
        const toastRef = { current: { show: vi.fn(), clear: vi.fn() } };
        
        const notifications=[
            { id: 1, title: "New Employee Invite", body: "Body", datetime: "2026-03-23T20:53:26" },
            { id: 2, title: "Employee Accepted Invite", body: "Body2", datetime: "2026-03-23T21:00:00" },
        ]

        render(
            <Header
                firstname="John"
                lastname="Smith"
                workspace="Test Workspace"
                sidebarVisible={true}
                setSidebarVisible={vi.fn()}
                toastRef={toastRef}
                notifications={notifications}
            />
        );

        const button = screen.getByTestId("notification-button");
        fireEvent.click(button);

        expect(toastRef.current.show).toHaveBeenCalledTimes(notifications.length);
    })


    // Test 5
    test("When a notification is deleted, there should no be a notification", async() => {
        const toastRef = React.createRef();

        render(
            <>
                <Toast ref={toastRef} position="top-right" />
                <Header
                    firstname="John"
                    lastname="Smith"
                    workspace="Test Workspace"
                    sidebarVisible={true}
                    setSidebarVisible={vi.fn()}
                    toastRef={toastRef}
                    notifications={[
                        { id: 1, title: "New Employee Invite", body: "Body", datetime: "2026-03-23T20:53:26" },
                    ]}
                />
            </>
            
        );

        const button = screen.getByTestId("notification-button");
        userEvent.click(button);

        const toastTitle = await screen.findByText("New Employee Invite");
        expect(toastTitle).toBeInTheDocument();

        const closeButton = document.querySelector(".p-toast-icon-close");
        expect(closeButton).toBeInTheDocument();
        userEvent.click(closeButton);

        await waitFor(() => {
            expect(document.querySelector(".p-toast-icon-close")).toBeNull();
        });
    })
})