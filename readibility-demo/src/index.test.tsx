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
		expect(text).toContain("Readability");
	});
});

describe("API Routes", () => {
	it("should return health status", async () => {
		const res = await app.request("/api/health");
		expect(res.status).toBe(200);
		const json = await res.json();
		expect(json.status).toBe("ok");
	});

	it("should return 400 for empty URLs", async () => {
		const res = await app.request("/api/scrape", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ urls: [] }),
		});
		expect(res.status).toBe(400);
	});

	it("should return 400 for more than 10 URLs", async () => {
		const urls = Array.from(
			{ length: 11 },
			(_, i) => `https://example${i}.com`,
		);
		const res = await app.request("/api/scrape", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ urls }),
		});
		expect(res.status).toBe(400);
	});

	it("should return 400 for missing analyze params", async () => {
		const res = await app.request("/api/analyze", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ htmlText: "test" }),
		});
		expect(res.status).toBe(400);
	});

	it("should analyze text pair", async () => {
		const res = await app.request("/api/analyze", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				htmlText: "<p>The quick brown fox jumps over the lazy dog.</p>",
				llmText: "The quick brown fox jumps over the lazy dog.",
			}),
		});
		expect(res.status).toBe(200);
		const json = await res.json();
		expect(json.result).toBeDefined();
		expect(json.result.html).toBeDefined();
		expect(json.result.llm).toBeDefined();
		expect(json.result.differences).toBeDefined();
	});
});
