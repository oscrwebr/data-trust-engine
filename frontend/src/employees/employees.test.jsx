import { afterEach, describe, expect, test, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within, waitFor, getByTestId, findByTestId } from "@testing-library/react";
import ViewEmployees from "./ViewEmployees";
import ManageEmployees from "./ManageEmployees";
import { MemoryRouter } from "react-router-dom";
import userEvent from "@testing-library/user-event";

const employees = [
    { user: { email:"alice@example.com", firstname:"Alice", surname:"Smith", user_id:1 }, role_name:"PII Role" },
    { user: { email:"bob@example.com", firstname:"Bob", surname:"Messi", user_id:2 }, role_name:"" },
    { user: { email:"charlie@example.com", firstname:"Charlie", surname:"Brown", user_id:3 }, role_name:"Legal Role" },
];

const pending_users = [
    { pending: {user_id: 4, email: 'valid@example.com', type: 'request'}, datetime: '2026-12-25T18:05:00'},
    { pending: {user_id: 5, email: 'test@email.com', type: 'invite'}, datetime: '2026-12-25T18:05:00'},
];

const roles = [
    {id: 1, name: "PII Role"}, {id: 2, name: "Financial Role"}
];

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
        expect(await screen.findByText("Send an Invite")).toBeInTheDocument();
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


    // Test 7
    test("Test that all elements for manage employees page load correctly", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        expect(await screen.findByText("Manage Employees")).toBeInTheDocument();
        expect(await screen.findByText("3 Active Employees")).toBeInTheDocument();
        expect(await screen.findByText("2 Pending Employees")).toBeInTheDocument();
        expect(await screen.findByText("Alice Smith")).toBeInTheDocument();
        expect(await screen.findByText("Charlie Brown")).toBeInTheDocument();
        expect(await screen.findByText("Bob Messi")).toBeInTheDocument();
        expect(await screen.findByText("valid@example.com")).toBeInTheDocument();
        expect(await screen.findByText("test@email.com")).toBeInTheDocument();
        expect(await screen.findByText("An invite was sent on the 25 December 2026 at 18:05:00")).toBeInTheDocument();
        expect(await screen.findByText("This employee has requested to join your workspace")).toBeInTheDocument();

    })


    // Test 8
    test("Test change display icon button works as expected", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
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


    // Test 9
    test("Test that remove button opens up correct modal", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const remove_button = await screen.findByTestId("remove-button-1")
        fireEvent.click(remove_button)

        expect(await screen.findByText("alice@example.com")).toBeInTheDocument();
        expect(await screen.findByText(/Are you sure you want to remove/)).toBeInTheDocument();
    })


    // Test 10
    test("Test that accept button opens up correct modal", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const accept_button = await screen.findByTestId("accept-button-valid@example.com")
        fireEvent.click(accept_button)

        const modal = await screen.findByRole("dialog");
        expect(within(modal).getByText("valid@example.com")).toBeInTheDocument();
        expect(within(modal).getByText(/An email containing an invite request will be sent to/)).toBeInTheDocument();
    })

    // Test 11
    test("Test that reject button opens up correct modal", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const reject_button = await screen.findByTestId("reject-button-valid@example.com")
        fireEvent.click(reject_button)

        const modal = await screen.findByRole("dialog");
        expect(within(modal).getByText("valid@example.com")).toBeInTheDocument();
        expect(within(modal).getByText(/Are you sure you want to reject/)).toBeInTheDocument();
    })

    // Test 12
    test("Test that filter by roles displays correct employees", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        api.get.mockResolvedValueOnce({
            data: roles,
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
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

    // Test 13
    test("Test that filter by status displays correct employees", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const trigger = await screen.findByRole("button", { name: /filter by status/i });
        await userEvent.click(trigger);

        const panel = await waitFor(() => {
            const el = document.querySelector(".p-dropdown-items-wrapper");
            if (!el) throw new Error("Dropdown not ready");
            return el;
        });

        expect(panel).toBeInTheDocument();
        const options = await screen.findAllByText(/pending/i);

        const dropdownOption = options.find(el =>
        el.classList.contains("p-dropdown-item-label")
        );

        if (!dropdownOption) {
        throw new Error("Dropdown option not found");
        }

        await userEvent.click(dropdownOption);

        

        await waitFor(() => {
            expect(screen.queryByText(/Bob\s+Messi/i)).not.toBeInTheDocument();
            expect(screen.queryByText(/Charlie\s+Brown/i)).not.toBeInTheDocument();
            expect(screen.queryByText(/Alice\s+Smith/i)).not.toBeInTheDocument();
        });
    })

    // Test 14
    test("Test that search by name/email displays correct employees", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const search = screen.getByPlaceholderText("Search by employee name or email");
        fireEvent.change(search, { target: { value: "alice" } });

        expect(await screen.findByText("Alice Smith")).toBeInTheDocument();
        expect(screen.queryByText("Charlie Brown")).not.toBeInTheDocument();
        expect(screen.queryByText("Bob Messi")).not.toBeInTheDocument();
    })

    // Test 15
    test("Test flow for updating and saving an employee's role", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        api.get.mockResolvedValueOnce({
            data: roles,
        });

        let toastCalled = null;
            const mockToast = {
            current: {
                show: (args) => { toastCalled = args; console.log("Toast triggered:", args); }
            }
        };

        api.put = vi.fn().mockResolvedValue({ status: 200 });

        render(
            <MemoryRouter>
                <ManageEmployees toast={ mockToast } />
            </MemoryRouter>
        );

        const employeeRow = await screen.findByTestId("row-1"); 

        const roleDropdown = within(employeeRow.closest("div")).getByTestId("row-role-dropdown");
        await userEvent.click(roleDropdown);

        const newRoleOption = await screen.findByText("Financial Role");
        await userEvent.click(newRoleOption);

        const saveButton = screen.getByTestId("save-information");
        await waitFor(() => expect(saveButton).not.toBeDisabled());

        await userEvent.click(saveButton);

        await waitFor(() => {
            expect(api.put).toHaveBeenCalledWith("/roles/update-user-roles", {
                employees: [{ user_id: 1, role_name: "Financial Role" }]
            });
        });
    })

    // Test 16
    test("Test confirm button for employee remove modal works as expected", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 

        api.delete = vi.fn().mockResolvedValue({ status: 200 });

        let toastCalled = null;
            const mockToast = {
            current: {
                show: (args) => { toastCalled = args; console.log("Toast triggered:", args); }
            }
        };

        render(
        <MemoryRouter>
            <ManageEmployees toast={mockToast} />
        </MemoryRouter>
        );

        const remove_button = await screen.findByTestId("remove-button-1");
        fireEvent.click(remove_button);

        const yes_button = await screen.findByText("Yes, remove employee");
        fireEvent.click(yes_button);

        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("The employee was removed from your workspace.");
        });

        await waitFor(() => {
            expect(api.delete).toHaveBeenCalledWith("/workspace/delete-user/1");
        });
        
        await waitFor(() => {
            expect(screen.queryByText(/Are you sure you want to remove/)).not.toBeInTheDocument();
        });
    })

    // Test 17
    test("Test cancel button for employee remove modal works as expected", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const remove_button = await screen.findByTestId("remove-button-1")
        fireEvent.click(remove_button)

        const cancel_button = await screen.findByRole("button", { name: /cancel/i });
        fireEvent.click(cancel_button)

        await waitFor(() => {
            expect(screen.queryByText(/Are you sure you want to remove/)).not.toBeInTheDocument();
        });
    })

    // Test 18
    test("Test confirm button for accept user modal works as expected", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 

        api.post = vi.fn().mockResolvedValue({
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
                <ManageEmployees toast={mockToast}/>
            </MemoryRouter>
        );

        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 7);
        if (expiryDate.getSeconds() >=500) {
            expiryDate.setMilliseconds(0);
            expiryDate.setSeconds(expiryDate.getSeconds() + 1);
        } else {
            expiryDate.setMilliseconds(0);
        }

        const accept_button = await screen.findByTestId("accept-button-valid@example.com")
        fireEvent.click(accept_button)

        const yes_button = await screen.findByText(/Yes, accept employee/i)
        fireEvent.click(yes_button)

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/invite/send-invite", {
                email: "valid@example.com",
                expiry_date: expiryDate.toISOString()
            });
        });

        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("An invite has been sent to the employee.");
        });

        await waitFor(() => {
            expect(screen.queryByText(/An email containing an invite request will be sent to/)).not.toBeInTheDocument();
        });
    })

    // Test 19
    test("Test confirm button for accept user modal outputs correct error message if invite email is invalid", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 

        api.post = vi.fn().mockResolvedValue({
            data: { success: "invalid" } 
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
                <ManageEmployees toast={mockToast}/>
            </MemoryRouter>
        );

        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 7);
        if (expiryDate.getSeconds() >=500) {
            expiryDate.setMilliseconds(0);
            expiryDate.setSeconds(expiryDate.getSeconds() + 1);
        } else {
            expiryDate.setMilliseconds(0);
        }

        const accept_button = await screen.findByTestId("accept-button-valid@example.com")
        fireEvent.click(accept_button)

        const yes_button = await screen.findByText(/Yes, accept employee/i)
        fireEvent.click(yes_button)

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/invite/send-invite", {
                email: "valid@example.com",
                expiry_date: expiryDate.toISOString()
            });
        });

        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("The email you are trying to send an invite to does not exist.");
        });

        await waitFor(() => {
            expect(screen.queryByText(/An email containing an invite request will be sent to/)).not.toBeInTheDocument();
        });
    })

    // Test 20
    test("Test confirm button for accept user modal outputs correct error message if invite email is untrustworthy", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 

        api.post = vi.fn().mockResolvedValue({
            data: { success: "trust" } 
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
                <ManageEmployees toast={mockToast}/>
            </MemoryRouter>
        );

        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 7);
        if (expiryDate.getSeconds() >=500) {
            expiryDate.setMilliseconds(0);
            expiryDate.setSeconds(expiryDate.getSeconds() + 1);
        } else {
            expiryDate.setMilliseconds(0);
        }

        const accept_button = await screen.findByTestId("accept-button-valid@example.com")
        fireEvent.click(accept_button)

        const yes_button = await screen.findByText(/Yes, accept employee/i)
        fireEvent.click(yes_button)

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/invite/send-invite", {
                email: "valid@example.com",
                expiry_date: expiryDate.toISOString()
            });
        });

        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("The email you are trying to send an invite to is untrustworthy.");
        });

        await waitFor(() => {
            expect(screen.queryByText(/An email containing an invite request will be sent to/)).not.toBeInTheDocument();
        });
    })

    // Test 21
    test("Test confirm button for accept user modal outputs correct error message if admin is sending too many invites", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 

        api.post = vi.fn().mockResolvedValue({
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
                <ManageEmployees toast={mockToast}/>
            </MemoryRouter>
        );

        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 7);
        expiryDate.setMilliseconds(0);  

        const accept_button = await screen.findByTestId("accept-button-valid@example.com")
        fireEvent.click(accept_button)

        const yes_button = await screen.findByText(/Yes, accept employee/i)
        fireEvent.click(yes_button)

        await waitFor(() => {
            expect(api.post).toHaveBeenCalledWith("/invite/send-invite", {
                email: "valid@example.com",
                expiry_date: expiryDate.toISOString()
            });
        });

        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("You are sending this employee too many invites, please try again tomorrow.");
        });

        await waitFor(() => {
            expect(screen.queryByText(/An email containing an invite request will be sent to/)).not.toBeInTheDocument();
        });
    })

    // Test 22
    test("Test cancel button for accept user modal works as expected", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const accept_button = await screen.findByTestId("accept-button-valid@example.com")
        fireEvent.click(accept_button)

        const cancel_button = await screen.findByRole("button", { name: /cancel/i });
        fireEvent.click(cancel_button)

        await waitFor(() => {
            expect(screen.queryByText(/An email containing an invite request will be sent to/)).not.toBeInTheDocument();
        });
    })

    // Test 23
    test("Test confirm button for reject user modal works as expected", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 

        api.patch = vi.fn().mockResolvedValue({ status: 200 });

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
                <ManageEmployees toast={mockToast}/>
            </MemoryRouter>
        );

        const reject_button = await screen.findByTestId("reject-button-valid@example.com")
        fireEvent.click(reject_button)

        const yes_button = await screen.findByText("Yes, reject employee")
        fireEvent.click(yes_button)

        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("The employee was rejected from your workspace.");
        });

        await waitFor(() => {
            expect(api.patch).toHaveBeenCalledWith("/workspace/reject-pending/4");
        });

        await waitFor(() => {
            expect(screen.queryByText(/Are you sure you want to reject/)).not.toBeInTheDocument();
        });
    })

    // Test 24
    test("Test cancel button for reject user modal works as expected", async() => {
        api.get.mockResolvedValueOnce({
            data: {
                active: employees,
                pending: pending_users
            }
        });

        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const reject_button = await screen.findByTestId("reject-button-valid@example.com")
        fireEvent.click(reject_button)

        const cancel_button = await screen.findByRole("button", { name: /cancel/i });
        fireEvent.click(cancel_button)

        await waitFor(() => {
            expect(screen.queryByText(/Are you sure you want to reject/)).not.toBeInTheDocument();
        });
    })

    // Test 25
    test("Check that ViewEmployees send invite button opens the send invite modal correctly", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 

        render(
            <MemoryRouter>
                <ViewEmployees />
            </MemoryRouter>
        );

        const send_invite_button = await screen.findByTestId("send-invite")
        fireEvent.click(send_invite_button)

        expect(await screen.findByText(/Send your employee an invite/i)).toBeInTheDocument();
    })

    // Test 25
    test("Check that ManageEmployees send invite button opens the send invite modal correctly", async() => {
        api.get
            .mockResolvedValueOnce({ data: { active: employees, pending: pending_users } }) 
            .mockResolvedValueOnce({ data: roles }); 


        render(
            <MemoryRouter>
                <ManageEmployees />
            </MemoryRouter>
        );

        const send_invite_button = await screen.findByTestId("send-invite")
        fireEvent.click(send_invite_button)

        expect(await screen.findByText(/Send your employee an invite/i)).toBeInTheDocument();
    })
})




