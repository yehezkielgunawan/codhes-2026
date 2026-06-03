import { describe, expect, it } from "vitest";
import { analyzeText, compareTexts } from "./analysis";

describe("analyzeText", () => {
	it("should calculate FRE for simple text", () => {
		const text = "The quick brown fox jumps over the lazy dog.";
		const result = analyzeText(text);
		expect(typeof result.fleschReadingEase).toBe("number");
		expect(result.fleschReadingEase).toBeGreaterThan(0);
	});

	it("should calculate FKGL for simple text", () => {
		const text = "The quick brown fox jumps over the lazy dog.";
		const result = analyzeText(text);
		expect(typeof result.fleschKincaidGradeLevel).toBe("number");
		expect(result.fleschKincaidGradeLevel).toBeGreaterThan(0);
	});

	it("should count tokens", () => {
		const text = "Hello world";
		const result = analyzeText(text);
		expect(typeof result.tokenCount).toBe("number");
		expect(result.tokenCount).toBeGreaterThan(0);
	});

	it("should calculate lexical density", () => {
		const text = "The cat sat on the mat.";
		const result = analyzeText(text);
		expect(typeof result.lexicalDensity).toBe("number");
		expect(result.lexicalDensity).toBeGreaterThanOrEqual(0);
		expect(result.lexicalDensity).toBeLessThanOrEqual(1);
	});
});

describe("compareTexts", () => {
	it("should compare two texts", () => {
		const htmlText = "<h1>Title</h1><p>The quick brown fox.</p>";
		const plainText = "Title\n\nThe quick brown fox.";
		const result = compareTexts(htmlText, plainText);

		expect(result.html).toBeDefined();
		expect(result.llm).toBeDefined();
		expect(result.differences).toBeDefined();
		expect(typeof result.differences.tokenCount.delta).toBe("number");
	});
});
