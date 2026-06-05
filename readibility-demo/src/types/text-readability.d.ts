declare module "text-readability" {
	interface Readability {
		fleschReadingEase(text: string): number;
		fleschKincaidGrade(text: string): number;
		gunningFog(text: string): number;
		smogIndex(text: string): number;
		colemanLiauIndex(text: string): number;
		automatedReadabilityIndex(text: string): number;
		daleChallReadabilityScore(text: string): number;
		linsearWriteFormula(text: string): number;
		textStandard(text: string, floatOutput?: boolean | null): string | number;
		textMedian(text: string): number;
		charCount(text: string, ignoreSpaces?: boolean): number;
		letterCount(text: string, ignoreSpaces?: boolean): number;
		lexiconCount(text: string, removePunctuation?: boolean): number;
		syllableCount(text: string, lang?: string): number;
		sentenceCount(text: string): number;
	}

	const readability: Readability;
	export default readability;
}
