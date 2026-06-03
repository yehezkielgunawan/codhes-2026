import { describe, expect, it } from "vitest";
import { extractMainContent } from "./scraper";

describe("extractMainContent", () => {
	it("should remove script and style tags", () => {
		const html = `
			<html>
				<head><style>body{color:red}</style></head>
				<body>
					<script>alert('xss')</script>
					<nav>Navigation</nav>
					<main>Main Content</main>
					<footer>Footer</footer>
				</body>
			</html>
		`;
		const result = extractMainContent(html);
		expect(result).not.toContain("script");
		expect(result).not.toContain("style");
		expect(result).not.toContain("Navigation");
		expect(result).not.toContain("Footer");
		expect(result).toContain("Main Content");
	});

	it("should fallback to body if no main/article", () => {
		const html = "<html><body><p>Hello World</p></body></html>";
		const result = extractMainContent(html);
		expect(result).toContain("Hello World");
	});

	it("should prioritize article over body", () => {
		const html = `
			<html>
				<body>
					<div>Header stuff</div>
					<article>Article Content Here</article>
					<div>Footer stuff</div>
				</body>
			</html>
		`;
		const result = extractMainContent(html);
		expect(result).toContain("Article Content Here");
	});

	it("should clean up whitespace", () => {
		const html =
			"<html><body><p>Hello    World</p><p>   Test   </p></body></html>";
		const result = extractMainContent(html);
		expect(result).not.toMatch(/\s{2,}/);
	});
});
