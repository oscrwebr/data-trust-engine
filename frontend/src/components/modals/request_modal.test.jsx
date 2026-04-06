import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Outlet, Routes, Route} from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import Dashboard from "../../Dashboard/Dashboard.jsx";
import RequestJoinWorkspaceModal from "./RequestJoinWorkspaceModal.jsx";

const workspaces = [
    {
        id: 1,
        name: "Workspace 1",
        image: "/workspace/image/1"
    },
    {
        id: 2,
        name: "Workspace 2",
        image: "/workspace/image/2"
    },
    {
        id: 3,
        name: "Workspace 3",
        image: "/workspace/image/3"
    }
]

// Provide Outlet context so useOutletContext works
function DashboardWithContext({ contextValue }) {
  return (
    <Routes>
      <Route path="/" element={<Outlet context={contextValue} />}>
        <Route index element={<Dashboard toast={() => {}} />} />
      </Route>
    </Routes>
  );
}

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

import api from "../../api/axiosConfig.js";

describe("Request Join Workspace Modal Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Test that correct information is displayed in the modal", async () => {

        render(
            <MemoryRouter>
                <RequestJoinWorkspaceModal visible={true}/>
            </MemoryRouter>
        );

        expect(screen.getByTestId("modal-header")).toBeInTheDocument();
        
        await waitFor(() => {
            expect(screen.queryByText(/Browse available workspaces below and send a request to join./i)).toBeInTheDocument();
            expect(screen.queryByText(/Send Request/i)).toBeInTheDocument();
        });

        expect(screen.getByTestId("workspace-dropdown")).toBeInTheDocument();
    })

    // Test 2
    test("Test error message when no workspace is sent", async () => {

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
                <RequestJoinWorkspaceModal visible={true} toast={mockToast}/>
            </MemoryRouter>
        );

        const accept_button = await screen.findByTestId("send-request-button")
        fireEvent.click(accept_button)
        
        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("You must select a valid workspace.");
        });
    })

    // Test 3
    test("Test success when the employee sends valid request", async () => {
        const mockSetVisible = vi.fn();

        api.get
            .mockResolvedValueOnce({ data: workspaces }) 
            
        api.post = vi.fn().mockResolvedValue({
            data: true
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
                <RequestJoinWorkspaceModal setVisible={mockSetVisible} visible={true} toast={mockToast}/>
            </MemoryRouter>
        );

        const modal = await screen.findByRole("dialog"); 

        const dropdown = within(modal.closest("div")).getByTestId("workspace-dropdown");
        await userEvent.click(dropdown);

        const option = await screen.findByText("Workspace 1");
        await userEvent.click(option);

        const accept_button = await screen.findByTestId("send-request-button")
        fireEvent.click(accept_button)

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/workspace/dashboard/request-join-workspace", {
                title: "New Invite Request",
                body: "An employee has requested join your workspace. You can review this request in Manage Employees.",
                workspace_id: 1,
            });
        });

        await waitFor(() => {
            expect(mockSetVisible).toHaveBeenCalledWith(false);
        });
    })
})