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

export async function fetchDocumentation(url: string): Promise<ScrapedData> {
	const urlObj = new URL(url);
	const name = urlObj.hostname.replace(/^www\./, "").split(".")[0];

	const htmlResponse = await fetch(url);
	if (!htmlResponse.ok) {
		throw new Error(`Failed to fetch HTML: ${htmlResponse.status}`);
	}
	const html = await htmlResponse.text();
	const htmlText = extractMainContent(html);

	const llmUrl = `${urlObj.protocol}//${urlObj.host}/llms.txt`;
	let llmText = "";

	try {
		const llmResponse = await fetch(llmUrl);
		if (llmResponse.ok) {
			llmText = await llmResponse.text();
		}
	} catch {
		// llms.txt not available
	}

	return { url, name, htmlText, llmText };
}

export async function fetchMultiple(urls: string[]): Promise<ScrapedData[]> {
	const results: ScrapedData[] = [];

	for (const url of urls) {
		try {
			const data = await fetchDocumentation(url);
			results.push(data);
		} catch (error) {
			console.error(`Error fetching ${url}:`, error);
		}
	}

	return results;
}
