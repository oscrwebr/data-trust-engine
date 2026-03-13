import { cleanup, fireEvent, render, screen, within, waitFor } from "@testing-library/react";
import { MemoryRouter, redirect, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import FileUpload from "./FileUpload.jsx";
import { useState } from "react";
import CreateWorkspace from "./CreateWorkspace.jsx";

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

import api from "../api/axiosConfig.js";

function FileUploadWrapper() {
  const [file, setFile] = useState([]);
  return <FileUpload file={file} setFile={setFile} />;
}

describe("Workspace Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });


    // Test 1
    test("Test all content in component loads correctly", async () => {
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
                <CreateWorkspace toast={mockToast} />
            </MemoryRouter>
        );

        expect(await screen.findByText("Create Your Workspace")).toBeInTheDocument();
        expect(await screen.findByText("Workspace Name")).toBeInTheDocument();
        expect(await screen.findByText("Upload Workspace Image")).toBeInTheDocument();
        expect(screen.getByTestId('file-upload')).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Enter workspace name")).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Create Workspace/i })).toBeInTheDocument();
        
    });

    // Test 2
    test("Test error message for null name", async () => {

        api.post = vi.fn().mockResolvedValue({ data: "name" });

        render(
            <MemoryRouter>
                <CreateWorkspace/>
            </MemoryRouter>
        );

        const modal = screen.getByRole('dialog');

        const submitButton = within(modal).getByRole('button', { name: /Create Workspace/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/workspace/create-workspace", expect.any(FormData));
        });

        const formData = api.post.mock.calls[0][1];
        expect(formData.get("name")).toBe(""); 
        expect(formData.get("image")).toBe(null);

        const errorMessage = await screen.findByText(/You must give your workspace a name\./i);
        expect(errorMessage).toBeInTheDocument();
    });

    // Test 3
    test("Test error message for null image", async () => {

        api.post = vi.fn().mockResolvedValue({ data: "image" });

        render(
            <MemoryRouter>
                <CreateWorkspace/>
            </MemoryRouter>
        );

        const modal = screen.getByRole('dialog');

        const emailInput = within(modal).getByPlaceholderText("Enter workspace name");
        fireEvent.change(emailInput, { target: { value: "Test Workspace" } });

        const submitButton = within(modal).getByRole('button', { name: /Create Workspace/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/workspace/create-workspace", expect.any(FormData));
        });

        const formData = api.post.mock.calls[0][1];
        expect(formData.get("name")).toBe("Test Workspace"); 
        expect(formData.get("image")).toBe(null);

        const errorMessage = await screen.findByText(/You must upload your workspace's image\./i);
        expect(errorMessage).toBeInTheDocument();
    });

    // Test 4
    test("Check file displays when an image file is added", async () => {
        render(<FileUploadWrapper />);

        const dropzone = screen.getByTestId("file-upload");
        const file = new File(["file content"], "workspace.png", { type: "image/png" });
        const input = dropzone.querySelector("input");
        await userEvent.upload(input, file);
        const fileName = await screen.findByText("workspace.png");
            expect(fileName).toBeInTheDocument();
        });

    // Test 5
    test("Check file is removed when remove button is clicked from preview", async () => {
        render(<FileUploadWrapper />);

        const dropzone = screen.getByTestId("file-upload");
        const file = new File(["content"], "workspace.png", { type: "image/png" });
        const input = dropzone.querySelector("input");
        await userEvent.upload(input, file);

        const removeButton = screen.getByTestId("file-remove");
        await userEvent.click(removeButton);

        expect(screen.queryByText("workspace.png")).not.toBeInTheDocument();
    });

    // Test 6
    test("Test success message and redirect with all valid inputs", async () => {

        let toastCalled = null;
        const mockToast = {
            current: {
                show: (args) => {
                    toastCalled = args;
                    console.log("Toast triggered:", args);
                },
            },
        };

        api.post = vi.fn().mockResolvedValue({ data: true });

        render(
            <MemoryRouter>
                <CreateWorkspace toast={mockToast} />
            </MemoryRouter>
        );
        
        const modal = screen.getByRole("dialog");

        const file = new File(["dummy content"], "workspace.png", { type: "image/png" });
        const dropzone = within(modal).getByTestId("file-upload");
        fireEvent.drop(dropzone, {
            dataTransfer: { files: [file], items: [file], types: ["Files"] }
        });

        const nameInput = within(modal).getByPlaceholderText("Enter workspace name");
        fireEvent.change(nameInput, { target: { value: "Test Workspace" } });

        const submitButton = within(modal).getByRole("button", { name: /Create Workspace/i });
        fireEvent.click(submitButton);
    
        await waitFor(() => {
            if (!toastCalled) {
                throw new Error("Toast was not triggered");
            }
            
            if (
                !toastCalled.detail.includes("Workspace successfully created!")
            ) {
                throw new Error("Toast called with wrong arguments");
            }
        })
    });
});