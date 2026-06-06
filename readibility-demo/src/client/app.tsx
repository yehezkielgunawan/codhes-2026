import { useEffect, useState } from "hono/jsx";
import { render } from "hono/jsx/dom";
import JSZip from "jszip";
import { BulkUrlInput } from "../components/BulkUrlInput";
import type { ComparisonResult } from "../lib/analysis";
import {
	clearResults,
	clearScrapedData,
	loadResults,
	loadScrapedData,
	saveResults,
	saveScrapedData,
} from "../lib/db";
import { exportCSV, exportMarkdown } from "../lib/export";
import type { ScrapedData } from "../lib/scraper";

interface ResultItem {
	name: string;
	url: string;
	result: ComparisonResult;
}

interface UrlInputGroupProps {
	value: string;
	onChange: (value: string) => void;
	onRemove: () => void;
	canRemove: boolean;
}

function UrlInputGroup({
	value,
	onChange,
	onRemove,
	canRemove,
}: UrlInputGroupProps) {
	return (
		<div class="flex gap-2">
			<input
				type="url"
				class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
				placeholder="https://example.com/docs"
				required
				value={value}
				onInput={(e) => onChange((e.target as HTMLInputElement).value)}
			/>
			{canRemove && (
				<button
					type="button"
					class="px-3 py-2 bg-red-100 text-red-600 rounded-md hover:bg-red-200 transition"
					onClick={onRemove}
				>
					×
				</button>
			)}
		</div>
	);
}

interface UrlFormProps {
	urls: string[];
	onUrlsChange: (urls: string[]) => void;
	onScrape: () => void;
	onAnalyze: () => void;
	onClear: () => void;
	isScraping: boolean;
	isAnalyzing: boolean;
	canAnalyze: boolean;
}

function UrlForm({
	urls,
	onUrlsChange,
	onScrape,
	onAnalyze,
	onClear,
	isScraping,
	isAnalyzing,
	canAnalyze,
}: UrlFormProps) {
	const handleAddUrl = () => {
		if (urls.length >= 10) {
			alert("Maximum 10 URLs allowed");
			return;
		}
		onUrlsChange([...urls, ""]);
	};

	const handleRemoveUrl = (index: number) => {
		onUrlsChange(urls.filter((_, i) => i !== index));
	};

	const handleUrlChange = (index: number, value: string) => {
		const newUrls = [...urls];
		newUrls[index] = value;
		onUrlsChange(newUrls);
	};

	return (
		<div class="bg-white rounded-lg shadow-md p-6 mb-6">
			<h2 class="text-xl font-semibold mb-4 text-gray-800">
				Documentation URLs
			</h2>
			<p class="text-sm text-gray-600 mb-4">
				Enter up to 10 documentation URLs. We'll automatically detect llms.txt
				files.
			</p>

			<div class="space-y-2 mb-4">
				{urls.map((url, index) => (
					<UrlInputGroup
						// biome-ignore lint/suspicious/noArrayIndexKey: URLs can be empty/duplicated, index is acceptable for this controlled form
						key={`url-${index}`}
						value={url}
						onChange={(value) => handleUrlChange(index, value)}
						onRemove={() => handleRemoveUrl(index)}
						canRemove={urls.length > 1}
					/>
				))}
			</div>

			<div class="flex gap-2">
				<button
					type="button"
					class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
					onClick={handleAddUrl}
				>
					+ Add URL
				</button>
			</div>

			<div class="mt-6 flex gap-3 flex-wrap">
				<button
					type="button"
					class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition disabled:opacity-50"
					disabled={isScraping || isAnalyzing}
					onClick={onScrape}
				>
					{isScraping ? "Scraping..." : "Scrape Documentation"}
				</button>

				<button
					type="button"
					class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition disabled:opacity-50"
					disabled={isScraping || isAnalyzing || !canAnalyze}
					onClick={onAnalyze}
				>
					{isAnalyzing ? "Analyzing..." : "Analyze"}
				</button>

				<button
					type="button"
					class="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
					onClick={onClear}
				>
					Clear All
				</button>
			</div>
		</div>
	);
}

interface ProgressBarProps {
	visible: boolean;
	progress: number;
	text: string;
}

function ProgressBar({ visible, progress, text }: ProgressBarProps) {
	if (!visible) return null;

	return (
		<div class="bg-white rounded-lg shadow-md p-6 mb-6">
			<h3 class="text-lg font-medium mb-3 text-gray-800">Progress</h3>
			<div class="w-full bg-gray-200 rounded-full h-4 mb-2">
				<div
					class="bg-blue-600 h-4 rounded-full transition-all duration-300"
					style={`width: ${progress}%`}
				/>
			</div>
			<p class="text-sm text-gray-600">{text}</p>
		</div>
	);
}

interface ResultsTableProps {
	results: ResultItem[];
	onExportMarkdown: () => void;
	onExportCSV: () => void;
}

function ResultsTable({
	results,
	onExportMarkdown,
	onExportCSV,
}: ResultsTableProps) {
	if (results.length === 0) return null;

	const metrics = [
		{ key: "tokenCount", label: "Token Count" },
		{ key: "fleschReadingEase", label: "Flesch Reading Ease" },
		{ key: "fleschKincaidGradeLevel", label: "FK Grade Level" },
		{ key: "lexicalDensity", label: "Lexical Density" },
		{ key: "gunningFog", label: "Gunning Fog" },
	];

	const avgTokenRatio =
		results.reduce((sum, r) => sum + r.result.differences.tokenCount.ratio, 0) /
		results.length;

	const avgFreChange =
		results.reduce(
			(sum, r) => sum + r.result.differences.fleschReadingEase.delta,
			0,
		) / results.length;

	return (
		<div class="bg-white rounded-lg shadow-md p-6">
			<h2 class="text-xl font-semibold mb-4 text-gray-800">Analysis Results</h2>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
				<div class="bg-blue-50 rounded-lg p-4">
					<h3 class="text-sm font-medium text-blue-800 mb-1">
						Avg Token Ratio
					</h3>
					<p class="text-2xl font-bold text-blue-600">
						{avgTokenRatio.toFixed(2)}x
					</p>
				</div>
				<div class="bg-green-50 rounded-lg p-4">
					<h3 class="text-sm font-medium text-green-800 mb-1">
						Avg FRE Change
					</h3>
					<p class="text-2xl font-bold text-green-600">
						{avgFreChange > 0 ? "+" : ""}
						{avgFreChange.toFixed(1)}
					</p>
				</div>
				<div class="bg-purple-50 rounded-lg p-4">
					<h3 class="text-sm font-medium text-purple-800 mb-1">Platforms</h3>
					<p class="text-2xl font-bold text-purple-600">{results.length}</p>
				</div>
			</div>

			<div class="overflow-x-auto">
				<table class="w-full text-sm text-left">
					<thead class="text-xs text-gray-700 uppercase bg-gray-100">
						<tr>
							<th class="px-4 py-3 rounded-tl-lg">Platform</th>
							<th class="px-4 py-3">Metric</th>
							<th class="px-4 py-3">HTML</th>
							<th class="px-4 py-3">llm.txt</th>
							<th class="px-4 py-3">Difference</th>
							<th class="px-4 py-3 rounded-tr-lg">% Change</th>
						</tr>
					</thead>
					<tbody>
						{results.map((item) =>
							metrics.map((metric, metricIndex) => {
								const diff = item.result.differences[metric.key];
								return (
									<tr
										key={`${item.name}-${metric.key}`}
										class="border-b hover:bg-gray-50"
									>
										<td
											class={`px-4 py-3 font-medium ${metricIndex === 0 ? "" : "text-gray-400"}`}
										>
											{metricIndex === 0 ? item.url : ""}
										</td>
										<td class="px-4 py-3">{metric.label}</td>
										<td class="px-4 py-3">{diff.html.toFixed(2)}</td>
										<td class="px-4 py-3">{diff.llm.toFixed(2)}</td>
										<td
											class={`px-4 py-3 ${diff.delta > 0 ? "text-green-600" : "text-red-600"}`}
										>
											{diff.delta > 0 ? "+" : ""}
											{diff.delta.toFixed(2)}
										</td>
										<td
											class={`px-4 py-3 ${diff.percentChange > 0 ? "text-green-600" : "text-red-600"}`}
										>
											{diff.percentChange > 0 ? "+" : ""}
											{diff.percentChange.toFixed(1)}%
										</td>
									</tr>
								);
							}),
						)}
					</tbody>
				</table>
			</div>

			<div class="flex gap-3 mt-6">
				<button
					type="button"
					class="px-4 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition"
					onClick={onExportMarkdown}
				>
					Export Markdown
				</button>
				<button
					type="button"
					class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-500 transition"
					onClick={onExportCSV}
				>
					Export CSV
				</button>
			</div>
		</div>
	);
}

export function App() {
	const [urls, setUrls] = useState<string[]>([""]);
	const [scrapedData, setScrapedData] = useState<ScrapedData[]>([]);
	const [results, setResults] = useState<ResultItem[]>([]);
	const [isScraping, setIsScraping] = useState(false);
	const [isAnalyzing, setIsAnalyzing] = useState(false);
	const [progressVisible, setProgressVisible] = useState(false);
	const [progress, setProgress] = useState(0);
	const [progressText, setProgressText] = useState("");
	const [inputMode, setInputMode] = useState<"single" | "bulk">("single");

	useEffect(() => {
		loadResults()
			.then((saved) => {
				if (saved.length > 0) {
					setResults(saved);
				}
			})
			.catch((error) => {
				console.error("Failed to load saved results:", error);
			});

		loadScrapedData()
			.then((saved) => {
				if (saved.length > 0) {
					setScrapedData(saved);
				}
			})
			.catch((error) => {
				console.error("Failed to load saved scraped data:", error);
			});
	}, []);

	const handleScrape = async () => {
		const validUrls = urls.filter((url) => url.trim().length > 0);

		if (validUrls.length === 0) {
			alert("Please enter at least one URL");
			return;
		}

		setIsScraping(true);
		setProgressVisible(true);
		setProgress(0);
		setProgressText("Starting...");

		try {
			const response = await fetch("/api/scrape", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ urls: validUrls }),
			});

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}`);
			}

			const data = await response.json();
			setScrapedData(data.results);

			for (let i = 0; i <= data.results.length; i++) {
				const percent = (i / validUrls.length) * 100;
				setProgress(percent);
				setProgressText(`${i} / ${validUrls.length} URLs processed`);
				await new Promise((resolve) => setTimeout(resolve, 100));
			}

			await saveScrapedData(
				data.results.map((r: ScrapedData) => ({
					...r,
					timestamp: Date.now(),
				})),
			);

			alert(`Scraped ${data.results.length} URLs successfully!`);
		} catch (error) {
			console.error("Scraping failed:", error);
			alert(
				`Scraping failed: ${error instanceof Error ? error.message : "Unknown error"}`,
			);
		} finally {
			setIsScraping(false);
		}
	};

	const handleAnalyze = async () => {
		if (scrapedData.length === 0) {
			alert("Please scrape documentation first");
			return;
		}

		setIsAnalyzing(true);
		setProgressVisible(true);
		setProgress(0);
		setProgressText("Starting analysis...");
		setResults([]);

		const newResults: ResultItem[] = [];

		try {
			for (let i = 0; i < scrapedData.length; i++) {
				const data = scrapedData[i];

				if (!data.llmText || data.llmText.length === 0) {
					console.warn(`No llm.txt found for ${data.name}`);
					continue;
				}

				const response = await fetch("/api/analyze", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						htmlText: data.htmlText,
						llmText: data.llmText,
					}),
				});

				if (!response.ok) continue;

				const result = await response.json();
				newResults.push({
					name: data.name,
					url: data.url,
					result: result.result,
				});

				setResults([...newResults]);

				const percent = ((i + 1) / scrapedData.length) * 100;
				setProgress(percent);
				setProgressText(`${i + 1} / ${scrapedData.length} analyzed`);
			}

			await saveResults(
				newResults.map((r) => ({
					...r,
					timestamp: Date.now(),
				})),
			);

			alert("Analysis complete!");
		} catch (error) {
			console.error("Analysis failed:", error);
			alert(
				`Analysis failed: ${error instanceof Error ? error.message : "Unknown error"}`,
			);
		} finally {
			setIsAnalyzing(false);
		}
	};

	const handleClear = async () => {
		if (!confirm("Clear all data?")) return;

		setUrls([""]);
		setScrapedData([]);
		setResults([]);
		setProgressVisible(false);

		await clearResults();
		await clearScrapedData();
	};

	const handleExportMarkdown = () => {
		if (results.length === 0) {
			alert("No results to export. Please analyze documentation first.");
			return;
		}
		exportMarkdown(results);
	};

	const handleExportCSV = () => {
		if (results.length === 0) {
			alert("No results to export. Please analyze documentation first.");
			return;
		}
		exportCSV(results);
	};

	const handleDownloadScrapedData = async () => {
		if (scrapedData.length === 0) {
			alert("No scraped data to download. Please scrape documentation first.");
			return;
		}

		try {
			const zip = new JSZip();
			const folder = zip.folder("scraped-data");

			if (!folder) {
				throw new Error("Failed to create zip folder");
			}

			for (const data of scrapedData) {
				folder.file(`${data.name}.html.txt`, data.htmlText);

				if (data.llmText) {
					folder.file(`${data.name}.llm.txt`, data.llmText);
				}
			}

			const blob = await zip.generateAsync({ type: "blob" });
			const url = URL.createObjectURL(blob);
			const link = document.createElement("a");
			link.href = url;
			link.download = `scraped-data-${new Date().toISOString().split("T")[0]}.zip`;
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
			URL.revokeObjectURL(url);
		} catch (error) {
			console.error("Failed to create zip:", error);
			alert(
				`Failed to create zip: ${error instanceof Error ? error.message : "Unknown error"}`,
			);
		}
	};

	const handleBulkUrlsParsed = (parsedUrls: string[]) => {
		setUrls(parsedUrls);
		alert(`Loaded ${parsedUrls.length} URLs. You can now scrape them.`);
	};

	return (
		<div>
			<header class="mb-8 text-center">
				<h1 class="text-3xl font-bold text-gray-900 mb-2">
					Readability & Token Efficiency Analyzer
				</h1>
				<p class="text-gray-600">
					Compare HTML documentation vs llm.txt files for readability and token
					efficiency.
				</p>
			</header>

			<div class="mb-4 flex gap-2">
				<button
					type="button"
					class={`px-4 py-2 rounded-md transition ${inputMode === "single" ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"}`}
					onClick={() => setInputMode("single")}
				>
					Single Input
				</button>
				<button
					type="button"
					class={`px-4 py-2 rounded-md transition ${inputMode === "bulk" ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"}`}
					onClick={() => setInputMode("bulk")}
				>
					Bulk Paste
				</button>
			</div>

			{inputMode === "bulk" && (
				<BulkUrlInput onUrlsParsed={handleBulkUrlsParsed} />
			)}

			<UrlForm
				urls={urls}
				onUrlsChange={setUrls}
				onScrape={handleScrape}
				onAnalyze={handleAnalyze}
				onClear={handleClear}
				isScraping={isScraping}
				isAnalyzing={isAnalyzing}
				canAnalyze={scrapedData.length > 0}
			/>

			<ProgressBar
				visible={progressVisible}
				progress={progress}
				text={progressText}
			/>

			<ResultsTable
				results={results}
				onExportMarkdown={handleExportMarkdown}
				onExportCSV={handleExportCSV}
			/>

			{scrapedData.length > 0 && (
				<div class="bg-white rounded-lg shadow-md p-6 mt-6">
					<h2 class="text-xl font-semibold mb-4 text-gray-800">Scraped Data</h2>
					<p class="text-sm text-gray-600 mb-4">
						{scrapedData.length} documentation page
						{scrapedData.length !== 1 ? "s" : ""} scraped and saved locally.
					</p>
					<button
						type="button"
						class="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition"
						onClick={handleDownloadScrapedData}
					>
						Download All Scraped Data
					</button>
				</div>
			)}
		</div>
	);
}

const root = document.getElementById("root");
if (root) {
	render(<App />, root);
}
