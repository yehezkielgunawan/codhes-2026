import type { ComparisonResult } from "./analysis";

interface ExportData {
	name: string;
	url: string;
	result: ComparisonResult;
}

function getDefaultFilename(): string {
	const date = new Date().toISOString().split("T")[0];
	return `readability-analysis-${date}`;
}

function downloadFile(content: string, filename: string, type: string) {
	const blob = new Blob([content], { type });
	const url = URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = url;
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);
}

export function generateMarkdown(results: ExportData[]): string {
	const date = new Date().toISOString().split("T")[0];
	const filename = getDefaultFilename();

	// Calculate aggregate stats
	const metrics = [
		"tokenCount",
		"wordCount",
		"sentenceCount",
		"fleschReadingEase",
		"fleschKincaidGradeLevel",
		"gunningFog",
		"smogIndex",
		"colemanLiau",
		"automatedReadabilityIndex",
		"lexicalDensity",
	] as const;

	const stats = metrics.map((metric) => {
		const htmlValues = results.map((r) => r.result.differences[metric].html);
		const llmValues = results.map((r) => r.result.differences[metric].llm);
		const deltas = results.map((r) => r.result.differences[metric].delta);
		const ratios = results.map((r) => r.result.differences[metric].ratio);

		const avg = (arr: number[]) =>
			arr.reduce((sum, val) => sum + val, 0) / arr.length;

		return {
			metric,
			avgHtml: avg(htmlValues),
			avgLlm: avg(llmValues),
			avgDelta: avg(deltas),
			avgRatio: avg(ratios),
			minHtml: Math.min(...htmlValues),
			maxHtml: Math.max(...htmlValues),
			minLlm: Math.min(...llmValues),
			maxLlm: Math.max(...llmValues),
		};
	});

	let md = "# Readability Analysis Report\n\n";
	md += `**Generated:** ${date}\n\n`;
	md += `**Filename:** ${filename}\n\n`;

	// Summary
	md += "## Summary\n\n";
	md += `- **Platforms:** ${results.length}\n`;
	md += `- **Avg Token Ratio:** ${stats[0].avgRatio.toFixed(2)}x\n`;
	md += `- **Avg FRE Change:** ${stats[3].avgDelta > 0 ? "+" : ""}${stats[3].avgDelta.toFixed(1)}\n\n`;

	// Per-Platform Results
	md += "## Per-Platform Results\n\n";

	for (const item of results) {
		md += `### ${item.name}\n\n`;
		md += `**URL:** ${item.url}\n\n`;
		md += "| Metric | HTML | llm.txt | Difference | % Change |\n";
		md += "|--------|------|---------|------------|----------|\n";

		for (const metric of metrics) {
			const diff = item.result.differences[metric];
			const label = metric
				.replace(/([A-Z])/g, " $1")
				.replace(/^./, (str) => str.toUpperCase());
			md += `| ${label} | ${diff.html.toFixed(2)} | ${diff.llm.toFixed(2)} | ${diff.delta > 0 ? "+" : ""}${diff.delta.toFixed(2)} | ${diff.percentChange > 0 ? "+" : ""}${diff.percentChange.toFixed(1)}% |\n`;
		}

		md += "\n";
	}

	// Aggregate Statistics
	md += "## Aggregate Statistics\n\n";
	md +=
		"| Metric | Avg HTML | Avg llm.txt | Avg Difference | Min HTML | Max HTML | Min llm.txt | Max llm.txt |\n";
	md +=
		"|--------|----------|-------------|----------------|----------|----------|-------------|-------------|\n";

	for (const stat of stats) {
		const label = stat.metric
			.replace(/([A-Z])/g, " $1")
			.replace(/^./, (str) => str.toUpperCase());
		md += `| ${label} | ${stat.avgHtml.toFixed(2)} | ${stat.avgLlm.toFixed(2)} | ${stat.avgDelta > 0 ? "+" : ""}${stat.avgDelta.toFixed(2)} | ${stat.minHtml.toFixed(2)} | ${stat.maxHtml.toFixed(2)} | ${stat.minLlm.toFixed(2)} | ${stat.maxLlm.toFixed(2)} |\n`;
	}

	return md;
}

export function generateCSV(results: ExportData[]): string {
	const metrics = [
		"tokenCount",
		"wordCount",
		"sentenceCount",
		"fleschReadingEase",
		"fleschKincaidGradeLevel",
		"gunningFog",
		"smogIndex",
		"colemanLiau",
		"automatedReadabilityIndex",
		"lexicalDensity",
	] as const;

	// Header
	let csv = "Platform,URL";
	for (const metric of metrics) {
		csv += `,${metric}_html,${metric}_llm,${metric}_delta,${metric}_ratio,${metric}_percentChange`;
	}
	csv += "\n";

	// Data rows
	for (const item of results) {
		csv += `"${item.name}","${item.url}"`;
		for (const metric of metrics) {
			const diff = item.result.differences[metric];
			csv += `,${diff.html.toFixed(4)},${diff.llm.toFixed(4)},${diff.delta.toFixed(4)},${diff.ratio.toFixed(4)},${diff.percentChange.toFixed(4)}`;
		}
		csv += "\n";
	}

	return csv;
}

export function exportMarkdown(results: ExportData[]) {
	const content = generateMarkdown(results);
	const filename = `${getDefaultFilename()}.md`;
	downloadFile(content, filename, "text/markdown");
}

export function exportCSV(results: ExportData[]) {
	const content = generateCSV(results);
	const filename = `${getDefaultFilename()}.csv`;
	downloadFile(content, filename, "text/csv");
}
