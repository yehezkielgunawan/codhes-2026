import { Hono } from "hono";
import { compareTexts } from "../lib/analysis";
import { fetchMultiple } from "../lib/scraper";

const api = new Hono();

api.post("/scrape", async (c) => {
	const { urls } = await c.req.json<{ urls: string[] }>();

	if (!urls || !Array.isArray(urls) || urls.length === 0) {
		return c.json({ error: "URLs array required" }, 400);
	}

	if (urls.length > 10) {
		return c.json({ error: "Maximum 10 URLs allowed" }, 400);
	}

	try {
		const results = await fetchMultiple(urls);
		return c.json({ results });
	} catch (error) {
		return c.json(
			{
				error: error instanceof Error ? error.message : "Unknown error",
			},
			500,
		);
	}
});

api.post("/analyze", async (c) => {
	const { htmlText, llmText } = await c.req.json<{
		htmlText: string;
		llmText: string;
	}>();

	if (!htmlText || !llmText) {
		return c.json({ error: "Both htmlText and llmText required" }, 400);
	}

	try {
		const result = compareTexts(htmlText, llmText);
		return c.json({ result });
	} catch (error) {
		return c.json(
			{
				error: error instanceof Error ? error.message : "Unknown error",
			},
			500,
		);
	}
});

api.get("/health", (c) => {
	return c.json({ status: "ok", timestamp: new Date().toISOString() });
});

export default api;
