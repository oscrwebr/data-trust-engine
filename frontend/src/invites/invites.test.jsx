import { cleanup, fireEvent, render, screen, within, waitFor } from "@testing-library/react";
import { MemoryRouter, redirect, Route, Routes } from "react-router-dom";
import axios from 'axios';
import { afterEach, describe, expect, test, vi } from "vitest";
import EmployeeInviteError from "./error.jsx";
import Dashboard from "../dashboard/Dashboard.jsx";
import Home from "../home/home.jsx"

vi.mock("primereact/calendar", () => ({
            Calendar: ({ value, onChange }) => (
                <input
                data-testid="calendar-input"
                value={value || ""}
                onChange={(e) => onChange({ value: new Date(e.target.value) })}
                />
            )
        }));

import EmployeeInvite from "./invites.jsx";

vi.mock("axios");
describe("Invite Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });


    // Test 1
    test("Test all content in modal loads correctly", async () => {
        render(
            <MemoryRouter>
                <EmployeeInvite visible={true} setVisible={() => {}}/>
            </MemoryRouter>
        );

        expect(await screen.findByText("Send your employee an invite")).toBeInTheDocument();
        expect(await screen.findByText("Send an invite to an employee by specifying the recipient's email address. You can also set an expiry date for the invitation.")).toBeInTheDocument();
        expect(await screen.findByText("Enter your employee's email address")).toBeInTheDocument();
        expect(await screen.findByText("Select an expiry date for the invite")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Email address")).toBeInTheDocument();
        expect(await screen.findByText("Send Invite")).toBeInTheDocument();
    })


    // Test 2
    test("Test error message when no email is given", async () => {
        axios.post.mockResolvedValueOnce({
            data: { success: "invalid" }
        });

        render(
            <MemoryRouter>
                <EmployeeInvite visible={true} setVisible={() => {}}/>
            </MemoryRouter>
        );
        
        const modal = screen.getByRole('dialog');
        const submitButton = within(modal).getByRole('button', { name: /send invite/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledWith(
                'http://localhost:8000/invite/send-invite',
                {
                    email: null,
                    expiry_date: null,
                }
            );
        });

        await waitFor(async () => {
            const errorMessage = await screen.findByText((text) =>
                text.includes("This email address doesn't exist")
            );
            expect(errorMessage).toBeInTheDocument();
        });
    })

    // Test 3
    test("Test error message when an invalid email is given", async () => {
        axios.post.mockResolvedValueOnce({
            data: { success: "invalid" }
        });

        render(
            <MemoryRouter>
                <EmployeeInvite visible={true} setVisible={() => {}}/>
            </MemoryRouter>
        );
        
        const modal = screen.getByRole('dialog');
        const emailInput = within(modal).getByPlaceholderText("Email address");
        fireEvent.change(emailInput, { target: { value: "invalid@example.com" } });

        const submitButton = within(modal).getByRole('button', { name: /send invite/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledWith(
                'http://localhost:8000/invite/send-invite',
                {
                    email: 'invalid@example.com',
                    expiry_date: null,
                }
            );
        });

        await waitFor(async () => {
            const errorMessage = await screen.findByText((text) =>
                text.includes("This email address doesn't exist")
            );
            expect(errorMessage).toBeInTheDocument();
        });
    })


    // Test 4
    test("Test error message when no expiry date is given", async () => {
        axios.post.mockResolvedValueOnce({
            data: { success: "expiry" }
        });

        render(
            <MemoryRouter>
                <EmployeeInvite visible={true} setVisible={() => {}}/>
            </MemoryRouter>
        );
        
        const modal = screen.getByRole('dialog');
        const emailInput = within(modal).getByPlaceholderText("Email address");
        fireEvent.change(emailInput, { target: { value: "valid@example.com" } });

        const submitButton = within(modal).getByRole('button', { name: /send invite/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledWith(
                'http://localhost:8000/invite/send-invite',
                {
                    email: 'valid@example.com',
                    expiry_date: null,
                }
            );
        });

        await waitFor(async () => {
            const errorMessage = await screen.findByText((text) =>
                text.includes("No expiry date selected")
            );
            expect(errorMessage).toBeInTheDocument();
            expect(screen.getByTestId("email-valid-icon")).toBeInTheDocument();
        });
    })
    

    // Test 5
    test("Test success message when both inputs are valid", async () => {
        axios.post.mockResolvedValueOnce({
            data: { success: true }
        });

        let toastCalled = null;
        const mockToast = {
            current: {
            show: (args) => {
                toastCalled = args;
                console.log("Toast triggered:", args);
            },
            },
        };

        render(
            <MemoryRouter>
                <Dashboard toast={mockToast} />
            </MemoryRouter>
        );

        const inviteButton = screen.getByRole("button", { name: /invite employee/i });
        fireEvent.click(inviteButton);

        const modal = screen.getByRole("dialog");

        const emailInput = within(modal).getByPlaceholderText("Email address");
        fireEvent.change(emailInput, { target: { value: "valid@example.com" } });

        const calendarInput = within(modal).getByTestId("calendar-input");
        fireEvent.change(calendarInput, { target: { value: "2030-04-01" } });

        const submitButton = within(modal).getByRole("button", { name: /send invite/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledWith(
                'http://localhost:8000/invite/send-invite',
                {
                    email: 'valid@example.com',
                    expiry_date: new Date("2030-04-01").toISOString(),
                }
            );
        });

        await waitFor(() => {
            if (!toastCalled) {
                throw new Error("Toast was not triggered");
            }
            
            if (
                !toastCalled.detail.includes("Invite successfully sent")
            ) {
                throw new Error("Toast called with wrong arguments");
            }
        })
    })


    // Test 6
    test("Test correct information displayed when user redirected to invite expiry error page", async () => {
        render(
            <MemoryRouter initialEntries={["/invite-error/expired?date=2026-03-03"]}>
                <Routes>
                    <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
                </Routes>
            </MemoryRouter>
        )
        expect(screen.getByText("This invite link is no longer valid")).toBeInTheDocument();
        expect(screen.getByText("Return to home")).toBeInTheDocument();
        expect(screen.getByText("Request to join workspace")).toBeInTheDocument();
        expect(screen.getByText("The Data Trust Engine")).toBeInTheDocument();

        const paragraph = screen.getByText(/expired on the/i);

        expect(paragraph).toHaveTextContent("The invite that your supervisor sent you expired on the");
        expect(paragraph).toHaveTextContent("3 March 2026");
        expect(paragraph).toHaveTextContent("To access your workspace, please ask your supervisor to send a new invite link");
    })

    // Test 7
    test("Test correct information displayed when user redirected to invite used error page", async () => {
        render(
            <MemoryRouter initialEntries={["/invite-error/used"]}>
                <Routes>
                    <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
                </Routes>
            </MemoryRouter>
        )
        expect(screen.getByText("This invite link is no longer valid")).toBeInTheDocument();
        expect(screen.getByText("Return to home")).toBeInTheDocument();
        expect(screen.getByText("Request to join workspace")).toBeInTheDocument();
        expect(screen.getByText("The Data Trust Engine")).toBeInTheDocument();
        expect(screen.getByText("This invite that your supervisor sent you has already been used. To access your workspace, please ask your supervisor to send a new invite link.")).toBeInTheDocument();
    })


    // Test 8
    test("Test user is redirected to home when they click 'Return to home' from invite error page", async () => {

        let toastCalled = null;
        const mockToast = {
            current: {
                show: (args) => {
                    toastCalled = args;
                    console.log("Toast triggered:", args);
                },
            },
        };

        render(
            <MemoryRouter initialEntries={["/invite-error/used"]}>
                <Routes>
                    <Route path="/invite-error/:type" element={<EmployeeInviteError />} />
                    <Route path="/" element={<Home toast={mockToast}/>} />
                </Routes>
            </MemoryRouter>

        )
        
        fireEvent.click(screen.getByText("Return to home"));
        expect(await screen.findByText("Create a workspace")).toBeInTheDocument();

    })
})