import Sidebar from './Sidebar.jsx';
import Home from '../../home/home.jsx';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach } from 'vitest';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom/vitest';
import  api  from '../../api/axiosConfig.js';
import { getAccessToken, setAccessToken } from '../../Auth/authStore.js';
import MockAdapter from "axios-mock-adapter";
import { Component } from 'react';

// // Mock router 'useNavigate' and 'useLocation'
// const mockUseNavigate = vi.fn();
// vi.mock('react-router-dom', async () => {
//     const actual = await vi.importActual('react-router-dom')
//     return {
//         ...actual,
//         useNavigate: () => mockUseNavigate,
//     };
// });

describe("Tests for logout feature", () => {
    test("Test that when the user clicks signout on the dashboard, there is an axios call to '/auth/logout'", async () => {
        // Set the access token
        setAccessToken("logout-test-token");
        // Ensure that the access token was correctly set
        expect(getAccessToken()).toBe("logout-test-token");

        const mock = new MockAdapter(api);
        // Handle the axios calls that are made by the component on load via useEffect
        mock.onGet("/workspace/dashboard").reply(200, {
            "user": {
                "firstname": "John",
                "surname": "Smith",
                "email": "JSmithy@hotmail.com",
                "role": "admin"
            },
            "workspace": "Business",
            "id": 6,
            "image": "/workspace/image/6"
        });
        mock.onGet("/workspace/get-pending-employees").reply(200);
        // This is the Axios call that we are expecting to be made!
        mock.onPost("/auth/logout").reply(200);

        // Render the sidebar
        render(
        <MemoryRouter initialEntries={["/dashboard"]}>
            <Routes>
                <Route path="/dashboard" element={<Sidebar/>}/>
                <Route path="/" element={<Home/>}/>
            </Routes>
        </MemoryRouter>);
        // Click signout
        await userEvent.click(await screen.findByText("Sign-out"))
        
        // MAIN ASSERTIONS
        expect(mock.history.post[0].url).toBe("/auth/logout");
    }),
    test("Test that when signout button is clicked, the user's access token is set to null", async () => {
        // Set the access token
        setAccessToken("logout-test-token");
        // Ensure that the access token was correctly set
        expect(getAccessToken()).toBe("logout-test-token");

        const mock = new MockAdapter(api);
        // Handle the axios calls that are made by the component on load via useEffect
        mock.onGet("/workspace/dashboard").reply(200, {
            "user": {
                "firstname": "John",
                "surname": "Smith",
                "email": "JSmithy@hotmail.com",
                "role": "admin"
            },
            "workspace": "Business",
            "id": 6,
            "image": "/workspace/image/6"
        });
        mock.onGet("/workspace/get-pending-employees").reply(200);
        mock.onPost("/auth/logout").reply(200);

        // Render the sidebar
        render(
        <MemoryRouter initialEntries={["/dashboard"]}>
            <Routes>
                <Route path="/dashboard" element={<Sidebar/>}/>
                <Route path="/" element={<Home/>}/>
            </Routes>
        </MemoryRouter>);
        // Ensure that the button is there to sign out
        const buttons = await screen.findAllByText("Sign-out");
        await userEvent.click(buttons[0]);
        // ASSERTIONS
        expect(getAccessToken()).toBeNull();
    }),
    test("Test that user is navigated to the home page once they are signed out", async () => {
        // Set the access token
        setAccessToken("logout-test-token");
        // Ensure that the access token was correctly set
        expect(getAccessToken()).toBe("logout-test-token");

        const mock = new MockAdapter(api);
        // Handle the axios calls that are made by the component on load via useEffect
        mock.onGet("/workspace/dashboard").reply(200, {
            "user": {
                "firstname": "John",
                "surname": "Smith",
                "email": "JSmithy@hotmail.com",
                "role": "admin"
            },
            "workspace": "Business",
            "id": 6,
            "image": "/workspace/image/6"
        });
        mock.onGet("/workspace/get-pending-employees").reply(200);
        mock.onPost("/auth/logout").reply(200);

        // Render the sidebar
        render(
        <MemoryRouter initialEntries={["/dashboard"]}>
            <Routes>
                <Route path="/dashboard" element={<Sidebar/>}/>
                <Route path="/" element={<Home/>}/>
            </Routes>
        </MemoryRouter>);
        // Ensure that the button is there to sign out
        const buttons = await screen.findAllByText("Sign-out");
        await userEvent.click(buttons[0]);
        expect((await screen.findAllByText("The Data Trust Engine"))[0].textContent);
    }),
    test("Test that when signout is successful, the user is sent to the homepage with a success message", async () => {
        // Set the access token
        setAccessToken("logout-test-token");
        // Ensure that the access token was correctly set
        expect(getAccessToken()).toBe("logout-test-token");

        let toastCalled = null;
            const mockToast = {
            current: {
                show: (args) => { toastCalled = args; console.log("Toast triggered:", args); }
            }
        };

        const mock = new MockAdapter(api);
        // Handle the axios calls that are made by the component on load via useEffect
        mock.onGet("/workspace/dashboard").reply(200, {
            "user": {
                "firstname": "John",
                "surname": "Smith",
                "email": "JSmithy@hotmail.com",
                "role": "admin"
            },
            "workspace": "Business",
            "id": 6,
            "image": "/workspace/image/6"
        });
        mock.onGet("/workspace/get-pending-employees").reply(200);
        mock.onPost("/auth/logout").reply(200);

        // Render the sidebar
        render(
        <MemoryRouter initialEntries={["/dashboard"]}>
            <Routes>
                <Route path="/dashboard" element={<Sidebar/>}/>
                <Route path="/" element={<Home toast={mockToast}/>}/>
            </Routes>
        </MemoryRouter>);
        // Ensure that the button is there to sign out
        const buttons = await screen.findAllByText("Sign-out");
        await userEvent.click(buttons[0]);
        // Expect there to be a success message
        // expect(await screen.findAllByText("You have logged out successfully!"))
        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("You have logged out successfully!");
        });
    }),
    test("Test that when signout is unsuccessful, the user is sent to the homepage with an error message", async () => {
        // Set the access token
        setAccessToken("logout-test-token");
        // Ensure that the access token was correctly set
        expect(getAccessToken()).toBe("logout-test-token");

        let toastCalled = null;
            const mockToast = {
            current: {
                show: (args) => { toastCalled = args; console.log("Toast triggered:", args); }
            }
        };

        const mock = new MockAdapter(api);
        // Handle the axios calls that are made by the component on load via useEffect
        mock.onGet("/workspace/dashboard").reply(200, {
            "user": {
                "firstname": "John",
                "surname": "Smith",
                "email": "JSmithy@hotmail.com",
                "role": "admin"
            },
            "workspace": "Business",
            "id": 6,
            "image": "/workspace/image/6"
        });
        mock.onGet("/workspace/get-pending-employees").reply(200);
        mock.onPost("/auth/logout").reply(500);

        // Render the sidebar
        render(
        <MemoryRouter initialEntries={["/dashboard"]}>
            <Routes>
                <Route path="/dashboard" element={<Sidebar/>}/>
                <Route path="/" element={<Home toast={mockToast}/>}/>
            </Routes>
        </MemoryRouter>);
        // Ensure that the button is there to sign out
        const buttons = await screen.findAllByText("Sign-out");
        await userEvent.click(buttons[0]);
        // Expect there to be a success message
        // expect(await screen.findAllByText("An error occurred while logging out."))
        await waitFor(() => {
            expect(toastCalled).not.toBeNull();
            expect(toastCalled.detail).toContain("An error occurred while logging out.");
        });
    })
})