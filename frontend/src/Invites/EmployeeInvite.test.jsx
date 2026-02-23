import { cleanup, fireEvent, render, screen, within, waitFor, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import axios from 'axios';
import { afterEach, describe, expect, test, vi } from "vitest";

 vi.mock("primereact/calendar", () => ({
            Calendar: ({ value, onChange }) => (
                <input
                data-testid="calendar-input"
                value={value || ""}
                onChange={(e) => onChange({ value: new Date(e.target.value) })}
                />
            )
        }));

import EmployeeInvite from "./EmployeeInvite.jsx";

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

        render(
            <MemoryRouter>
                <EmployeeInvite visible={true} setVisible={() => {}}/>
            </MemoryRouter>
        );
        
        const modal = screen.getByRole('dialog');
        const emailInput = within(modal).getByPlaceholderText("Email address");
        fireEvent.change(emailInput, { target: { value: "valid@example.com" } });

        const calendarInput = within(modal).getByTestId("calendar-input");
        fireEvent.change(calendarInput, { target: { value: "2026-04-01" } });
    
        const submitButton = within(modal).getByRole('button', { name: /send invite/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledWith(
                'http://localhost:8000/invite/send-invite',
                {
                    email: 'valid@example.com',
                    expiry_date: new Date("2026-04-01").toISOString(),
                }
            );
        });

        await waitFor(async () => {
            expect(await screen.findByText("Invite successfully sent!")).toBeInTheDocument();
        });
    })
})