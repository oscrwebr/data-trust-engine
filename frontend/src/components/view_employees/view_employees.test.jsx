import RowCard from "./RowCard"
import SquareCard from "./SquareCard"
import SendMessage from "./SendMessage"
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within, waitFor } from "@testing-library/react";

const employees = [
    {user: {email:"alice@example.com", firstname: "Alice", oid: "oid1", role: "employee", surname: "Smith", user_id: 1}, role_name: 'PII Role'},
    {user: {email:"charlie@example.com", firstname: "Charlie", oid: "oid2", role: "employee", surname: "Brown", user_id: 2}, role_name: 'Legal Role'},
    {user: {email:"bob@example.com", firstname: "Bob", oid: "oid3", role: "employee", surname: "Messi", user_id: 3}, role_name: ''}
]

vi.mock("../../api/axiosConfig.js", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: [] }),
    post: vi.fn().mockResolvedValue({ data: { success: true } }), 
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  },
}));

import api from "../../api/axiosConfig";

describe("Components for View Employees", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Check that RowCard component loads correctly with props passed through", async() => {
        render(
            <MemoryRouter>
                <RowCard initials="TC" firstname="Tom" surname="Clapham" email="example@email.com" role="Legal Role" risk={{files: {id: 1, status: 'Risk Detected', flagged_files: []}}}/>
            </MemoryRouter>
        );

        expect(await screen.findByText("TC")).toBeInTheDocument();
        expect(await screen.findByText("Tom Clapham")).toBeInTheDocument();
        expect(await screen.findByText("example@email.com")).toBeInTheDocument();
        expect(await screen.findByText("Legal Role")).toBeInTheDocument();
    })


    // Test 2
    test("Check that SquareCard component loads correctly with props passed through", async() => {
        render(
            <MemoryRouter>
                <SquareCard initials="TC" firstname="Tom" surname="Clapham" email="example@email.com" role="Legal Role"/>
            </MemoryRouter>
        );

        expect(await screen.findByText("TC")).toBeInTheDocument();
        expect(await screen.findByText("Tom Clapham")).toBeInTheDocument();
        expect(await screen.findByText("example@email.com")).toBeInTheDocument();
        expect(await screen.findByText("Legal Role")).toBeInTheDocument();
    })


    // Test 3
    test("Check that SendMessage component loads correctly with props passed through", async() => {
        render(
            <MemoryRouter>
                <SendMessage visible={true} selectedEmployees={employees}/>
            </MemoryRouter>
        );

        expect(await screen.findByText("Alice Smith")).toBeInTheDocument();
        expect(await screen.findByText("Charlie Brown")).toBeInTheDocument();
        expect(await screen.findByText("Bob Messi")).toBeInTheDocument();
        expect(await screen.findByText("Send Message")).toBeInTheDocument();
        expect(await screen.findByText("Send your employees a message")).toBeInTheDocument();
    })


    // Test 4
    test("Check success toast appears when message is sent with body defined", async() => {
        api.post.mockResolvedValue({
            data: true
        });

        let toastCalls = [];
        const mockToast = {
            current: {
                show: (args) => {
                    toastCalls.push(args);
                    console.log("Toast triggered:", args);
                },
            },
        };

        render(
            <MemoryRouter>
                <SendMessage visible={true} selectedEmployees={employees} toast={mockToast}/>
            </MemoryRouter>
        );

        const modal = screen.getByRole("dialog");

        const textarea = within(modal).getByPlaceholderText("Enter the message you would like to send");
        fireEvent.change(textarea, { target: { value: "This is a test message" } });

        const send = within(modal).getByRole('button', { name: /Send Message/i });
        fireEvent.click(send);

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith(
                '/workspace/send-message',
                {
                    employees: [1, 2, 3],
                    body: "This is a test message"
                }
            );
        });

        // Check that the success toast is triggered correctly
        await waitFor(() => {
            const successToast = toastCalls.find(
                (t) => t.detail === "Message successfully sent!" 
            );
            expect(successToast).toBeDefined();
            expect(successToast.severity).toBe("success");
        });
    })


    // Test 5
    test("Check error toast appears when message is sent without a body", async() => {

        api.post.mockResolvedValue({
            data: null
        });

        let toastCalls = [];
        const mockToast = {
            current: {
                show: (args) => {
                    toastCalls.push(args);
                    console.log("Toast triggered:", args);
                },
            },
        };

        render(
            <MemoryRouter>
                <SendMessage visible={true} selectedEmployees={employees} toast={mockToast}/>
            </MemoryRouter>
        );

        const modal = screen.getByRole("dialog");

        const send = within(modal).getByRole('button', { name: /Send Message/i });
        fireEvent.click(send);

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith(
                '/workspace/send-message',
                {
                    employees: [1, 2, 3],
                    body: null
                }
            );
        });

        // Check that the success toast is triggered correctly
        await waitFor(() => {
            const successToast = toastCalls.find(
                (t) => t.detail === "You cannot send a message without a body." 
            );
            expect(successToast).toBeDefined();
            expect(successToast.severity).toBe("error");
        });
    })
})

