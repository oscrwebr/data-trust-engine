import { sortRoles } from "./sortRoles";
import { describe, expect, test } from "vitest";

const testRoles = [
    {
        id: 1,
        name: "Financial Role",
        last_updated: "2022-01-15",
    },
    {
        id: 2,
        name: "HR Role",
        last_updated: "2024-01-15",
    },
    {
        id: 3,
        name: "Employee",
        last_updated: "2023-01-15",
    },
];

describe("sortGames", () => {
    test("testCorrectlySortsByNameAscending", () => {
        const result = sortRoles(testRoles, "nameAscending").map((role) => role.name);
        expect(result).toEqual(["Employee", "Financial Role", "HR Role"]);
    });

    test("testCorrectlySortsByNameDescending", () => {
        const result = sortRoles(testRoles, "nameDescending").map((role) => role.name);
        expect(result).toEqual(["HR Role", "Financial Role", "Employee"]);
    });

    test("testCorrectlySortsByLastUpdatedNewestToOldest", () => {
        const result = sortRoles(testRoles, "newestToOldest").map((role) => role.name);
        expect(result).toEqual(["HR Role", "Employee", "Financial Role"]);
    });

    test("testCorrectlySortsByLastUpdatedDateOldestToNewest", () => {
        const result = sortRoles(testRoles, "oldestToNewest").map((role) => role.name);
        expect(result).toEqual(["Financial Role", "Employee", "HR Role"]);
    });
})