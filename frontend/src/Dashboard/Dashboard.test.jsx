import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import Dashboard from "./Dashboard.jsx";

vi.mock("../api/axiosConfig.js", () => ({
  default: {
    get: vi.fn((url) => {
      if (url === "/workspace/dashboard") {
        return Promise.resolve({
          data: {
            user: {
              firstname: "John",
              surname: "Doe",
              email: "john@example.com",
              role: "admin"
            },
            workspace: "Test Workspace"
          }
        });
      }
      if (url === "/workspace/get-notifications") {
        return Promise.resolve({ data: [] });
      }
      if (url === "/workspace/get-workspace-image") {
        return Promise.resolve({
          data: new Blob(["fake image"], { type: "image/png" })
        });
      }
    }),
    post: vi.fn(() => Promise.resolve({}))
  }
}));

global.URL.createObjectURL = vi.fn(() => "mock-url");

describe("Dashboard Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Test that correct information is displayed on dashboard", async () => {
        render(
            <MemoryRouter>
                <Dashboard />
            </MemoryRouter>
        );

        expect(screen.getByTestId("dashboard-h1")).toBeInTheDocument();
    })
})