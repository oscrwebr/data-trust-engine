import { afterEach, describe, expect, test, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within, waitFor, getByTestId, findByTestId } from "@testing-library/react";
import ViewEmployees from "./ViewEmployees";
import { MemoryRouter } from "react-router-dom";
import userEvent from "@testing-library/user-event";

const employees = [
    { user: { email:"alice@example.com", firstname:"Alice", surname:"Smith", user_id:1 }, role_name:"PII Role" },
    { user: { email:"bob@example.com", firstname:"Bob", surname:"Messi", user_id:2 }, role_name:"" },
    { user: { email:"charlie@example.com", firstname:"Charlie", surname:"Brown", user_id:3 }, role_name:"Legal Role" },
]

const roles = [
    {id: 1, name: "PII Role"}
]

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

describe("View Employees Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
        cleanup();
    });

    // Test 1
    test("Check that ViewEmployees component loads correctly with data", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees
            }
        });

        render(
            <MemoryRouter>
                <ViewEmployees />
            </MemoryRouter>
        );

        expect(await screen.findByText("View Employees")).toBeInTheDocument();
        expect(await screen.findByText("3 People")).toBeInTheDocument();
        expect(await screen.findByText("Alice Smith")).toBeInTheDocument();
        expect(await screen.findByText("Charlie Brown")).toBeInTheDocument();
        expect(await screen.findByText("Bob Messi")).toBeInTheDocument();
        expect(await screen.findByText("Send a Message")).toBeInTheDocument();
    })


    // Test 2
    test("Check correct card arrangement is displayed when clicking display icon", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees
            }
        });

        render(
            <MemoryRouter>
                <ViewEmployees />
            </MemoryRouter>
        );

        expect(await screen.findByTestId("row-1")).toBeInTheDocument();
        expect(await screen.findByTestId("row-2")).toBeInTheDocument();
        expect(await screen.findByTestId("row-3")).toBeInTheDocument();

        const button = await screen.findByTestId("display-change-button");
        fireEvent.click(button);

        expect(await screen.findByTestId("square-1")).toBeInTheDocument();
        expect(await screen.findByTestId("square-2")).toBeInTheDocument();
        expect(await screen.findByTestId("square-3")).toBeInTheDocument();
    })


    // Test 3
    test("Check that clicking individual checkbox performs correct actions", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees
            }
        });

        render(
            <MemoryRouter>
                <ViewEmployees />
            </MemoryRouter>
        );

        const checkbox = await screen.findByTestId("checkbox-1")
        const selectAllInput = within(checkbox).getByRole("checkbox");
        const button = await screen.findByTestId("send-message-button")

        expect(selectAllInput).not.toBeChecked();
        expect(button).toBeDisabled();

        fireEvent.click(selectAllInput);

        expect(button).not.toBeDisabled();
        expect(selectAllInput).toBeChecked();

    })


    // Test 4
    test("Check that search bar works as expected and returns correct row", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees
            }
        });

        render(
            <MemoryRouter>
                <ViewEmployees />
            </MemoryRouter>
        );

        const search = screen.getByPlaceholderText("Search by employee name or email");
        fireEvent.change(search, { target: { value: "alice" } });

        expect(await screen.findByText("Alice Smith")).toBeInTheDocument();
        expect(screen.queryByText("Charlie Brown")).not.toBeInTheDocument();
        expect(screen.queryByText("Bob Messi")).not.toBeInTheDocument();

    })


    // Test 5
    test("Check that filter by role works as expected and returns correct row", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
            }
        });

        api.get.mockResolvedValueOnce({
            data: roles,
        });

        render(
            <MemoryRouter>
                <ViewEmployees />
            </MemoryRouter>
        );

        const trigger = await screen.findByRole("button", { name: /filter by roles/i });
        await userEvent.click(trigger);

        const panel = await waitFor(() => {
            const el = document.querySelector(".p-dropdown-items-wrapper");
            if (!el) throw new Error("Dropdown not ready");
            return el;
        });

        expect(panel).toBeInTheDocument();
        const options = await screen.findAllByText(/pii role/i);

        const dropdownOption = options.find(el =>
        el.classList.contains("p-dropdown-item-label")
        );

        if (!dropdownOption) {
        throw new Error("Dropdown option not found");
        }

        await userEvent.click(dropdownOption);

        await waitFor(() => {
            expect(screen.getByText(/Alice\s+Smith/i)).toBeInTheDocument();
            expect(screen.queryByText(/Bob\s+Messi/i)).not.toBeInTheDocument();
            expect(screen.queryByText(/Charlie\s+Brown/i)).not.toBeInTheDocument();
        });
    })

    // Test 6
    test("Check clicking select all performs correct actions", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees
            }
        });

        render(
            <MemoryRouter>
                <ViewEmployees />
            </MemoryRouter>
        );

        const checkbox_1 = await screen.findByTestId("checkbox-1")
        const checkbox_1_input = within(checkbox_1).getByRole("checkbox");

        const checkbox_2 = await screen.findByTestId("checkbox-2")
        const checkbox_2_input = within(checkbox_2).getByRole("checkbox");

        const checkbox_3 = await screen.findByTestId("checkbox-3")
        const checkbox_3_input = within(checkbox_3).getByRole("checkbox");

        const button = await screen.findByTestId("send-message-button")

        expect(checkbox_1_input).not.toBeChecked();
        expect(checkbox_2_input).not.toBeChecked();
        expect(checkbox_3_input).not.toBeChecked();
        expect(button).toBeDisabled();


        const selectAllWrapper = await screen.findByTestId("select-all-checkbox");
        const selectAllInput = within(selectAllWrapper).getByRole("checkbox");
        fireEvent.click(selectAllInput);

        expect(checkbox_1_input).toBeChecked();
        expect(checkbox_2_input).toBeChecked();
        expect(checkbox_3_input).toBeChecked();
        expect(button).not.toBeDisabled();

    })
})

