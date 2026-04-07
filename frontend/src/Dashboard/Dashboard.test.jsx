import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Outlet, Routes, Route} from "react-router-dom";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import Dashboard from "./Dashboard.jsx";

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

import api from "../api/axiosConfig";

describe("Dashboard Component", () => {
    beforeEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Test that correct information is displayed on dashboard for an admin", async () => {

        // Define contextValue here!
        const contextValue = {
          toastNotifications: { current: { show: () => {} } },
          setVisible: () => {},
          setNotifications: () => {},
          user: {
            firstname: "John",
            surname: "Doe",
            email: "john@example.com",
            role: "admin",
          },
          workspace: {
            name: "Workspace 1",
            id: 123,
            image: "/workspace/image/123"
          }
        };

        render(
            <MemoryRouter initialEntries={["/"]}>
                <DashboardWithContext contextValue={contextValue} />
            </MemoryRouter>
        );

        expect(await screen.findByTestId("dashboard-h1")).toBeInTheDocument();
    })

    // Test 2
    test("Test that correct information is displayed on dashboard for an employee", async () => {

        // Define contextValue here!
        const contextValue = {
          toastNotifications: { current: { show: () => {} } }, // mimic Toast ref
          setVisible: () => {},
          setNotifications: () => {},
          user: {
            firstname: "John",
            surname: "Doe",
            email: "john@example.com",
            role: "employee",
          },
          workspace: null
        };

        render(
            <MemoryRouter initialEntries={["/"]}>
                <DashboardWithContext contextValue={contextValue} />
            </MemoryRouter>
        );

        expect(await screen.findByTestId("dashboard-h1")).toBeInTheDocument();
        expect(await screen.findByText("Request to Join Workspace")).toBeInTheDocument();
    })

    // Test 3
    test("Test that modal appears when you click the request join button", async () => {

        // Define contextValue here!
        const contextValue = {
          toastNotifications: { current: { show: () => {} } },
          setVisible: () => {},
          setNotifications: () => {},
          user: {
            firstname: "John",
            surname: "Doe",
            email: "john@example.com",
            role: "employee",
          },
          workspace: null
        };

        render(
            <MemoryRouter initialEntries={["/"]}>
                <DashboardWithContext contextValue={contextValue} />
            </MemoryRouter>
        );

        expect(await screen.findByTestId("dashboard-h1")).toBeInTheDocument();

        const accept_button = await screen.findByTestId("request-join-workspace-button")
        fireEvent.click(accept_button)

        await waitFor(() => {
            expect(screen.queryByText(/Browse available workspaces below and send a request to join./i)).toBeInTheDocument();
        });
    })
})