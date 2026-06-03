import { encodingForModel } from "js-tiktoken";
import readability from "text-readability";

const encoder = encodingForModel("gpt-4o");

export interface AnalysisResult {
	tokenCount: number;
	wordCount: number;
	sentenceCount: number;
	fleschReadingEase: number;
	fleschKincaidGradeLevel: number;
	gunningFog: number;
	smogIndex: number;
	colemanLiau: number;
	automatedReadabilityIndex: number;
	lexicalDensity: number;
}

export interface ComparisonResult {
	html: AnalysisResult;
	llm: AnalysisResult;
	differences: {
		[key: string]: {
			html: number;
			llm: number;
			delta: number;
			ratio: number;
			percentChange: number;
		};
	};
}

const STOPWORDS = new Set([
	"the",
	"a",
	"an",
	"and",
	"or",
	"but",
	"in",
	"on",
	"at",
	"to",
	"for",
	"of",
	"with",
	"by",
	"is",
	"are",
	"was",
	"were",
	"be",
	"been",
	"being",
	"have",
	"has",
	"had",
	"do",
	"does",
	"did",
	"will",
	"would",
	"could",
	"should",
	"may",
	"might",
	"must",
	"shall",
	"can",
	"it",
	"this",
	"that",
	"these",
	"those",
	"i",
	"you",
	"he",
	"she",
	"we",
	"they",
	"me",
	"him",
	"her",
	"us",
	"them",
	"my",
	"your",
	"his",
	"its",
	"our",
	"their",
]);

function calculateLexicalDensity(text: string): number {
	const words = text.toLowerCase().match(/\b[a-z]+\b/g) || [];
	if (words.length === 0) return 0;

	const contentWords = words.filter((word) => !STOPWORDS.has(word));
	return contentWords.length / words.length;
}

export function analyzeText(text: string): AnalysisResult {
	const tokens = encoder.encode(text);
	const tokenCount = tokens.length;

	const fleschReadingEase = readability.fleschReadingEase(text);
	const fleschKincaidGradeLevel = readability.fleschKincaidGrade(text);
	const gunningFog = readability.gunningFog(text);
	const smogIndex = readability.smogIndex(text);
	const colemanLiau = readability.colemanLiauIndex(text);
	const automatedReadabilityIndex = readability.automatedReadabilityIndex(text);
	const lexicalDensity = calculateLexicalDensity(text);

	const words = text.match(/\b\w+\b/g) || [];
	const sentences = text.split(/[.!?]+/).filter((s) => s.trim().length > 0);

	return {
		tokenCount,
		wordCount: words.length,
		sentenceCount: sentences.length,
		fleschReadingEase,
		fleschKincaidGradeLevel,
		gunningFog,
		smogIndex,
		colemanLiau,
		automatedReadabilityIndex,
		lexicalDensity,
	};
}

export function compareTexts(
	htmlText: string,
	llmText: string,
): ComparisonResult {
	const html = analyzeText(htmlText);
	const llm = analyzeText(llmText);

	const differences: ComparisonResult["differences"] = {};

	for (const key of Object.keys(html) as Array<keyof AnalysisResult>) {
		const htmlValue = html[key];
		const llmValue = llm[key];

		differences[key] = {
			html: htmlValue,
			llm: llmValue,
			delta: llmValue - htmlValue,
			ratio: htmlValue !== 0 ? llmValue / htmlValue : 0,
			percentChange:
				htmlValue !== 0 ? ((llmValue - htmlValue) / htmlValue) * 100 : 0,
		};
	}

	return { html, llm, differences };
}
