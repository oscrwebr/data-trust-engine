import { vi, expect, describe, beforeEach, forEach, test } from 'vitest';
import MockAdapter from "axios-mock-adapter";
import  api  from './axiosConfig.js';

describe("Tests for axios interceptors", () => {
    test("check that when a user makes a request to a protected endpoint, the interceptor automatically redirects to the authentication endpoint", async () => {
        const mock = new MockAdapter(api);

        mock.onGet("/auth/test").reply(401)
        mock.onGet("/auth/token/refresh").reply(200, {access_token: "new access_token"})

        await api.get("/auth/test")
        .then(res => {})
        .catch(error => {})

        expect(mock.history.get[1].url).toBe("/auth/token/refresh")
    }),

    test("When an unauthenticated user makes a request to a protected resource, they should be redirected to the refresh endpoint and then on success, the original request should be retried", async () => {
        const mock = new MockAdapter(api);

        mock.onGet("/auth/test").reply(401)
        mock.onGet("/auth/token/refresh").reply(200, {access_token: "new access_token"})
        
        await api.get("/auth/test")
        .then(res => {})
        .catch(error => {})

        expect(mock.history.get[2].url).toBe("/auth/test") // Test that it is the same as the original

    }),

    test("When a user makes a request to any endpoint other than \"/auth/sign-in\" there should be a bearer token in the authorization header (access token)", async () => {
        const mock = new MockAdapter(api);

        await api.get("/auth/test")
        .then(res => {})
        .catch(error => {})

        expect(mock.history.get[0].headers.Authorization).not.toBeUndefined()

    }),

    test("When a user makes a request to \"/auth/sign-in\" there should NOT be a bearer token in the authorization header", async () => {
        const mock = new MockAdapter(api);

        await api.get("/auth/sign-in")
        .then(res => {})
        .catch(error => {})

        expect(mock.history.get[0].headers.Authorization).toBeUndefined()

    }),

    test("When an authenticated user makes a request to a protected resource, there should be no redirections to refresh or sign in endpoints", async () => {
        const mock = new MockAdapter(api);

        mock.onGet("/auth/test").reply(200);
        
        await api.get("/auth/test")
        .then(res => {})
        .catch(error => {})

        expect(mock.history.get.length).toBe(1);
    }),

    test("When a user has no access or refresh token, they should be sent to the sign in page if trying to access a protected resource", async () => {
        const mock = new MockAdapter(api);

        mock.onGet("/auth/test").reply(401);
        mock.onGet("/auth/token/refresh").reply(401);

        await api.get("/auth/test")
        .then(res => {})
        .catch(error => {})

        // Check that the length of the response is only 2 get requests, because instead of using axios, it uses window.location.href to follow the backend response
        expect(mock.history.get.length).toBe(2)

    })
}) 