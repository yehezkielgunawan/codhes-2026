import { describe, expect, it } from "vitest";
import app from "./index";

describe("App", () => {
	it("should return 200 on GET /", async () => {
		const res = await app.request("/");
		expect(res.status).toBe(200);
	});

	it("should return HTML content on GET /", async () => {
		const res = await app.request("/");
		const text = await res.text();
		expect(text).toContain("Hello!");
	});
});
