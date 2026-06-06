import * as cheerio from "cheerio";

export interface ScrapedData {
	url: string;
	name: string;
	htmlText: string;
	llmText: string;
}

export function extractMainContent(html: string): string {
	const $ = cheerio.load(html);

	$(
		"script, style, nav, header, footer, aside, [role='banner'], [role='navigation'], [role='complementary']",
	).remove();

	const selectors = [
		"main",
		"article",
		"[role='main']",
		".content",
		"#content",
		".documentation",
		"#documentation",
		".docs-content",
		"#docs-content",
	];

	for (const selector of selectors) {
		const element = $(selector).first();
		if (element.length > 0) {
			const text = element.text().replace(/\s+/g, " ").trim();
			if (text.length > 100) {
				return text;
			}
		}
	}

	return $("body").text().replace(/\s+/g, " ").trim();
}

function fetchWithTimeout(url: string, timeoutMs = 10000): Promise<Response> {
	const controller = new AbortController();
	const timeout = setTimeout(() => controller.abort(), timeoutMs);

	return fetch(url, { signal: controller.signal }).finally(() =>
		clearTimeout(timeout),
	);
}

export async function fetchDocumentation(url: string): Promise<ScrapedData> {
	const urlObj = new URL(url);
	const name = urlObj.hostname.replace(/^www\./, "").split(".")[0];

	const htmlResponse = await fetchWithTimeout(url);
	if (!htmlResponse.ok) {
		throw new Error(`Failed to fetch HTML: ${htmlResponse.status}`);
	}
	const html = await htmlResponse.text();
	const htmlText = extractMainContent(html);

	const llmUrl = `${urlObj.protocol}//${urlObj.host}/llms.txt`;
	let llmText = "";

	try {
		const llmResponse = await fetchWithTimeout(llmUrl, 5000);
		if (llmResponse.ok) {
			llmText = await llmResponse.text();
		}
	} catch {
		// llms.txt not available
	}

	return { url, name, htmlText, llmText };
}

export async function fetchMultiple(urls: string[]): Promise<ScrapedData[]> {
	const results = await Promise.allSettled(
		urls.map((url) => fetchDocumentation(url)),
	);

	const scraped: ScrapedData[] = [];
	for (let i = 0; i < results.length; i++) {
		const result = results[i];
		if (result.status === "fulfilled") {
			scraped.push(result.value);
		} else {
			console.error(`Error fetching ${urls[i]}:`, result.reason);
		}
	}

	return scraped;
}
