import { describe, expect, it } from "vitest";
import type { ComparisonResult } from "./analysis";
import { generateCSV, generateMarkdown } from "./export";

const mockResults = [
	{
		name: "FastAPI",
		url: "https://fastapi.tiangolo.com/",
		result: {
			html: {
				tokenCount: 5000,
				wordCount: 3000,
				sentenceCount: 200,
				fleschReadingEase: 45.2,
				fleschKincaidGradeLevel: 12.5,
				gunningFog: 15.3,
				smogIndex: 14.1,
				colemanLiau: 11.2,
				automatedReadabilityIndex: 10.8,
				lexicalDensity: 0.55,
			},
			llm: {
				tokenCount: 2100,
				wordCount: 3000,
				sentenceCount: 200,
				fleschReadingEase: 52.1,
				fleschKincaidGradeLevel: 10.2,
				gunningFog: 12.1,
				smogIndex: 11.5,
				colemanLiau: 9.8,
				automatedReadabilityIndex: 8.9,
				lexicalDensity: 0.62,
			},
			differences: {
				tokenCount: {
					html: 5000,
					llm: 2100,
					delta: -2900,
					ratio: 0.42,
					percentChange: -58,
				},
				wordCount: {
					html: 3000,
					llm: 3000,
					delta: 0,
					ratio: 1,
					percentChange: 0,
				},
				sentenceCount: {
					html: 200,
					llm: 200,
					delta: 0,
					ratio: 1,
					percentChange: 0,
				},
				fleschReadingEase: {
					html: 45.2,
					llm: 52.1,
					delta: 6.9,
					ratio: 1.15,
					percentChange: 15.3,
				},
				fleschKincaidGradeLevel: {
					html: 12.5,
					llm: 10.2,
					delta: -2.3,
					ratio: 0.82,
					percentChange: -18.4,
				},
				gunningFog: {
					html: 15.3,
					llm: 12.1,
					delta: -3.2,
					ratio: 0.79,
					percentChange: -20.9,
				},
				smogIndex: {
					html: 14.1,
					llm: 11.5,
					delta: -2.6,
					ratio: 0.82,
					percentChange: -18.4,
				},
				colemanLiau: {
					html: 11.2,
					llm: 9.8,
					delta: -1.4,
					ratio: 0.88,
					percentChange: -12.5,
				},
				automatedReadabilityIndex: {
					html: 10.8,
					llm: 8.9,
					delta: -1.9,
					ratio: 0.82,
					percentChange: -17.6,
				},
				lexicalDensity: {
					html: 0.55,
					llm: 0.62,
					delta: 0.07,
					ratio: 1.13,
					percentChange: 12.7,
				},
			},
		} as ComparisonResult,
	},
];

describe("generateMarkdown", () => {
	it("should generate markdown with headers", () => {
		const md = generateMarkdown(mockResults);
		expect(md).toContain("# Readability Analysis Report");
		expect(md).toContain("## Summary");
		expect(md).toContain("## Per-Platform Results");
		expect(md).toContain("## Aggregate Statistics");
	});

	it("should include platform name", () => {
		const md = generateMarkdown(mockResults);
		expect(md).toContain("### FastAPI");
		expect(md).toContain("https://fastapi.tiangolo.com/");
	});

	it("should include metrics table", () => {
		const md = generateMarkdown(mockResults);
		expect(md).toContain("| Metric | HTML | llm.txt | Difference | % Change |");
		expect(md).toContain("Token Count");
		expect(md).toContain("Flesch Reading Ease");
	});

	it("should include aggregate stats", () => {
		const md = generateMarkdown(mockResults);
		expect(md).toContain("| Metric | Avg HTML | Avg llm.txt |");
	});

	it("should include date in filename", () => {
		const md = generateMarkdown(mockResults);
		const date = new Date().toISOString().split("T")[0];
		expect(md).toContain(`readability-analysis-${date}`);
	});
});

describe("generateCSV", () => {
	it("should generate CSV with header", () => {
		const csv = generateCSV(mockResults);
		expect(csv).toContain("Platform,URL");
		expect(csv).toContain("tokenCount_html,tokenCount_llm");
	});

	it("should include platform data", () => {
		const csv = generateCSV(mockResults);
		expect(csv).toContain("FastAPI");
		expect(csv).toContain("https://fastapi.tiangolo.com/");
	});

	it("should include all metrics", () => {
		const csv = generateCSV(mockResults);
		expect(csv).toContain("5000.0000");
		expect(csv).toContain("2100.0000");
		expect(csv).toContain("-2900.0000");
	});

	it("should be wide format", () => {
		const csv = generateCSV(mockResults);
		const lines = csv.trim().split("\n");
		// Header + 1 data row
		expect(lines).toHaveLength(2);
	});
});
