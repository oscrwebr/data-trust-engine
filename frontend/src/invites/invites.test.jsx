import { cleanup, fireEvent, render, screen, within, waitFor } from "@testing-library/react";
import { MemoryRouter, redirect, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import EmployeeInviteError from "./error.jsx";
import Dashboard from "../dashboard/Dashboard.jsx";
import WorkspaceJoinedError from "./WorkspaceJoined.jsx";
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

const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

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

global.URL.createObjectURL = vi.fn(() => "mock-url");

import api from "../api/axiosConfig.js";

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
        api.post.mockResolvedValueOnce({
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
            expect(api.post).toHaveBeenCalledWith(
                '/invite/send-invite',
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
        api.post.mockResolvedValueOnce({
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
            expect(api.post).toHaveBeenCalledWith(
                '/invite/send-invite',
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
        api.post.mockResolvedValueOnce({
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
            expect(api.post).toHaveBeenCalledWith(
                '/invite/send-invite',
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
        api.post.mockResolvedValueOnce({
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
                <Dashboard toast={mockToast}/>
                <EmployeeInvite visible={true} setVisible={() => {}} toast={mockToast}/>
            </MemoryRouter>
        );

        const modal = screen.getByRole("dialog");

        const emailInput = within(modal).getByPlaceholderText("Email address");
        fireEvent.change(emailInput, { target: { value: "valid@example.com" } });

        const calendarInput = within(modal).getByTestId("calendar-input");
        fireEvent.change(calendarInput, { target: { value: "2030-04-01" } });

        const submitButton = within(modal).getByRole("button", { name: /send invite/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith(
                '/invite/send-invite',
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
    test("Test correct information displayed when user redirected to workspace already joined modal", async () => {
        render(
            <MemoryRouter initialEntries={["/workspace-joined"]}>
                <Routes>
                    <Route path="/workspace-joined" element={<WorkspaceJoinedError />} />
                </Routes>
            </MemoryRouter>
        )
        expect(screen.getByText("You've already joined a workspace")).toBeInTheDocument();
        expect(screen.getByText("Return to home")).toBeInTheDocument();
        expect(screen.getByText("Go to my workspace")).toBeInTheDocument();
        expect(screen.getByText("The Data Trust Engine")).toBeInTheDocument();
        expect(screen.getByText("It looks like you’ve already joined this workspace. Click “Go to my workspace” to log in and access it. If this seems incorrect, contact your workspace administrator.")).toBeInTheDocument();
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
            <MemoryRouter initialEntries={["/workspace-joined"]}>
                <Routes>
                    <Route path="/workspace-joined" element={<WorkspaceJoinedError />} />
                    <Route path="/" element={<Home toast={mockToast}/>} />
                </Routes>
            </MemoryRouter>

        )
        
        fireEvent.click(screen.getByText("Return to home"));
        expect(await screen.findByText("Create a workspace")).toBeInTheDocument();

    })

    // Test 9
    test("Test for users who will have logged in to accept invite are redirected to home & see success message", async () => {

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
            <MemoryRouter initialEntries={["/?toast=signup"]}>
                <Routes>
                    <Route path="/" element={<Home toast={mockToast}/>} />
                </Routes>
            </MemoryRouter>
        )
        
        expect(await screen.findByText("Create a workspace")).toBeInTheDocument();
        await waitFor(() => {
            if (!toastCalled) {
                throw new Error("Toast was not triggered");
            }
            
            if (
                !toastCalled.detail.includes("You have joined your workspace!")
            ) {
                throw new Error("Toast called with wrong arguments");
            }
        })
    })

    // Test 10
    test("Test that sending 2 back to back invites will throw an error toast message on screen", async() => {
        api.post.mockResolvedValueOnce({
            data: { success: "cooldown" }
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
                <Dashboard toast={mockToast}/>
                <EmployeeInvite visible={true} setVisible={() => {}} toast={mockToast}/>
            </MemoryRouter>
        );

        const modal = screen.getByRole("dialog");

        const emailInput = within(modal).getByPlaceholderText("Email address");
        fireEvent.change(emailInput, { target: { value: "valid@example.com" } });

        const calendarInput = within(modal).getByTestId("calendar-input");
        fireEvent.change(calendarInput, { target: { value: "2030-04-01" } });

        const submitButton = within(modal).getByRole("button", { name: /send invite/i });

        // Click the button twice
        fireEvent.click(submitButton);
        fireEvent.click(submitButton);

        await waitFor(() => {
            if (!toastCalled) {
                throw new Error("Toast was not triggered");
            }
            
            if (
                !toastCalled.detail.includes("You are sending this employee too many invites, please try again tomorrow.")
            ) {
                throw new Error("Toast called with wrong arguments");
            }
        })
    })

    // Test 11
    test("Test error message when an admin sends an invite to themselves", async () => {
        api.post.mockResolvedValueOnce({
            data: { success: "admin" }
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
                <Dashboard toast={mockToast}/>
                <EmployeeInvite visible={true} setVisible={() => {}} toast={mockToast}/>
            </MemoryRouter>
        );

        const modal = screen.getByRole("dialog");

        const emailInput = within(modal).getByPlaceholderText("Email address");
        fireEvent.change(emailInput, { target: { value: "valid@example.com" } });

        const calendarInput = within(modal).getByTestId("calendar-input");
        fireEvent.change(calendarInput, { target: { value: "2030-04-01" } });

        const submitButton = within(modal).getByRole("button", { name: /send invite/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            if (!toastCalled) {
                throw new Error("Toast was not triggered");
            }
            
            if (
                !toastCalled.detail.includes("You cannot send an invite to yourself.")
            ) {
                throw new Error("Toast called with wrong arguments");
            }
        })
    })

    // Test 12
    test("Test that clicking go to my workspace button correctly navigates user to dashboard", async () => {
        render(
            <MemoryRouter>
                <WorkspaceJoinedError />
            </MemoryRouter>
        );

        const button = screen.getByText("Go to my workspace");
        fireEvent.click(button);
        
        expect(mockNavigate).toHaveBeenCalledWith("/dashboard");
    })

    // Test 13
    test("Test request to join workspace button functions correctly", async () => {
        api.post.mockResolvedValueOnce({
            data: { success: true }
        });

        const title = "New Invite Request";
        const body = "An employee has requested join your workspace. You can review this request in Manage Employees.";

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
            <MemoryRouter initialEntries={["/invite-error/expired?date=2026-03-03&workspace=1"]}>
                <Routes>
                    <Route path="/invite-error/:type" element={<EmployeeInviteError toast={mockToast}/>} />
                </Routes>
            </MemoryRouter>
        )

        const request_button = screen.getByRole("button", { name: /Request to join workspace/i });
        fireEvent.click(request_button);

        expect(request_button).toBeDisabled();

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/workspace/request-join-workspace",
                {
                    title: title,
                    body: body,
                    workspace_id: "1",
                }
            );
        });

        await waitFor(() => {
            if (!toastCalled) {
                throw new Error("Toast was not triggered");
            }
            
            if (
                !toastCalled.detail.includes("Invite request sent!")
            ) {
                throw new Error("Toast called with wrong arguments");
            }
        })
    })
})