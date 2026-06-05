import type { ComparisonResult } from "../lib/analysis";
import { clearResults, loadResults, saveResults } from "../lib/db";
import { exportCSV, exportMarkdown } from "../lib/export";
import type { ScrapedData } from "../lib/scraper";

interface AppState {
	urls: string[];
	scrapedData: ScrapedData[];
	results: { name: string; url: string; result: ComparisonResult }[];
	isScraping: boolean;
	isAnalyzing: boolean;
}

const state: AppState = {
	urls: [],
	scrapedData: [],
	results: [],
	isScraping: false,
	isAnalyzing: false,
};

function getElement<T extends HTMLElement>(id: string): T {
	const el = document.getElementById(id);
	if (!el) throw new Error(`Element #${id} not found`);
	return el as T;
}

function init() {
	loadSavedResults();

	getElement<HTMLButtonElement>("add-url-btn").addEventListener(
		"click",
		addUrlInput,
	);
	getElement<HTMLButtonElement>("scrape-btn").addEventListener(
		"click",
		startScraping,
	);
	getElement<HTMLButtonElement>("analyze-btn").addEventListener(
		"click",
		startAnalysis,
	);
	getElement<HTMLButtonElement>("clear-btn").addEventListener(
		"click",
		clearAll,
	);
	getElement<HTMLButtonElement>("export-md-btn").addEventListener(
		"click",
		exportMarkdownHandler,
	);
	getElement<HTMLButtonElement>("export-csv-btn").addEventListener(
		"click",
		exportCSVHandler,
	);

	bindRemoveButtons();
}

function addUrlInput() {
	const urlList = getElement<HTMLDivElement>("url-list");
	const inputs = urlList.querySelectorAll(".url-input-group");

	if (inputs.length >= 10) {
		alert("Maximum 10 URLs allowed");
		return;
	}

	const newGroup = document.createElement("div");
	newGroup.className = "url-input-group flex gap-2";
	newGroup.innerHTML = `
		<input
			type="url"
			class="url-input flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
			placeholder="https://example.com/docs"
			required
		/>
		<button type="button" class="remove-url-btn px-3 py-2 bg-red-100 text-red-600 rounded-md hover:bg-red-200 transition">
			×
		</button>
	`;

	urlList.appendChild(newGroup);
	bindRemoveButtons();
}

function bindRemoveButtons() {
	const buttons = document.querySelectorAll(".remove-url-btn");
	for (const btn of buttons) {
		btn.removeEventListener("click", removeUrlInput);
		btn.addEventListener("click", removeUrlInput);
	}
}

function removeUrlInput(event: Event) {
	const btn = event.target as HTMLButtonElement;
	const group = btn.closest(".url-input-group");
	if (group) group.remove();
}

function getUrls(): string[] {
	const inputs = document.querySelectorAll<HTMLInputElement>(".url-input");
	return Array.from(inputs)
		.map((input) => input.value.trim())
		.filter((url) => url.length > 0);
}

async function startScraping() {
	const urls = getUrls();

	if (urls.length === 0) {
		alert("Please enter at least one URL");
		return;
	}

	state.urls = urls;
	state.isScraping = true;
	updateUI();

	const progressContainer = getElement<HTMLDivElement>("progress-container");
	const progressBar = getElement<HTMLDivElement>("progress-bar");
	const progressText = getElement<HTMLParagraphElement>("progress-text");

	progressContainer.classList.remove("hidden");

	try {
		const response = await fetch("/api/scrape", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ urls }),
		});

		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}

		const data = await response.json();
		state.scrapedData = data.results;

		for (let i = 0; i <= state.scrapedData.length; i++) {
			const percent = (i / urls.length) * 100;
			progressBar.style.width = `${percent}%`;
			progressText.textContent = `${i} / ${urls.length} URLs processed`;
			await new Promise((resolve) => setTimeout(resolve, 100));
		}

		getElement<HTMLButtonElement>("analyze-btn").disabled = false;

		alert(`Scraped ${state.scrapedData.length} URLs successfully!`);
	} catch (error) {
		console.error("Scraping failed:", error);
		alert(
			`Scraping failed: ${error instanceof Error ? error.message : "Unknown error"}`,
		);
	} finally {
		state.isScraping = false;
		updateUI();
	}
}

async function startAnalysis() {
	if (state.scrapedData.length === 0) {
		alert("Please scrape documentation first");
		return;
	}

	state.isAnalyzing = true;
	updateUI();

	const progressContainer = getElement<HTMLDivElement>("progress-container");
	const progressBar = getElement<HTMLDivElement>("progress-bar");
	const progressText = getElement<HTMLParagraphElement>("progress-text");

	progressContainer.classList.remove("hidden");
	state.results = [];

	try {
		for (let i = 0; i < state.scrapedData.length; i++) {
			const data = state.scrapedData[i];

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
			state.results.push({
				name: data.name,
				url: data.url,
				result: result.result,
			});

			const percent = ((i + 1) / state.scrapedData.length) * 100;
			progressBar.style.width = `${percent}%`;
			progressText.textContent = `${i + 1} / ${state.scrapedData.length} analyzed`;
		}

		await saveResults(
			state.results.map((r) => ({
				...r,
				timestamp: Date.now(),
			})),
		);

		displayResults();

		alert("Analysis complete!");
	} catch (error) {
		console.error("Analysis failed:", error);
		alert(
			`Analysis failed: ${error instanceof Error ? error.message : "Unknown error"}`,
		);
	} finally {
		state.isAnalyzing = false;
		updateUI();
	}
}

function displayResults() {
	const resultsContainer = getElement<HTMLDivElement>("results-container");
	const resultsBody = getElement<HTMLTableSectionElement>("results-body");
	const summaryCards = getElement<HTMLDivElement>("summary-cards");

	resultsContainer.classList.remove("hidden");
	resultsBody.innerHTML = "";

	for (const item of state.results) {
		const diffs = item.result.differences;
		const metrics = [
			{ key: "tokenCount", label: "Token Count" },
			{ key: "fleschReadingEase", label: "Flesch Reading Ease" },
			{ key: "fleschKincaidGradeLevel", label: "FK Grade Level" },
			{ key: "lexicalDensity", label: "Lexical Density" },
			{ key: "gunningFog", label: "Gunning Fog" },
		];

		for (let i = 0; i < metrics.length; i++) {
			const metric = metrics[i];
			const diff = diffs[metric.key];

			const row = document.createElement("tr");
			row.className = "border-b hover:bg-gray-50";
			row.innerHTML = `
				<td class="px-4 py-3 font-medium ${i === 0 ? "" : "text-gray-400"}">
					${i === 0 ? item.name : ""}
				</td>
				<td class="px-4 py-3">${metric.label}</td>
				<td class="px-4 py-3">${diff.html.toFixed(2)}</td>
				<td class="px-4 py-3">${diff.llm.toFixed(2)}</td>
				<td class="px-4 py-3 ${diff.delta > 0 ? "text-green-600" : "text-red-600"}">
					${diff.delta > 0 ? "+" : ""}${diff.delta.toFixed(2)}
				</td>
				<td class="px-4 py-3 ${diff.percentChange > 0 ? "text-green-600" : "text-red-600"}">
					${diff.percentChange > 0 ? "+" : ""}${diff.percentChange.toFixed(1)}%
				</td>
			`;
			resultsBody.appendChild(row);
		}
	}

	if (state.results.length > 0) {
		const avgTokenRatio =
			state.results.reduce(
				(sum, r) => sum + r.result.differences.tokenCount.ratio,
				0,
			) / state.results.length;

		const avgFreChange =
			state.results.reduce(
				(sum, r) => sum + r.result.differences.fleschReadingEase.delta,
				0,
			) / state.results.length;

		summaryCards.innerHTML = `
			<div class="bg-blue-50 rounded-lg p-4">
				<h3 class="text-sm font-medium text-blue-800 mb-1">Avg Token Ratio</h3>
				<p class="text-2xl font-bold text-blue-600">${avgTokenRatio.toFixed(2)}x</p>
			</div>
			<div class="bg-green-50 rounded-lg p-4">
				<h3 class="text-sm font-medium text-green-800 mb-1">Avg FRE Change</h3>
				<p class="text-2xl font-bold text-green-600">${avgFreChange > 0 ? "+" : ""}${avgFreChange.toFixed(1)}</p>
			</div>
			<div class="bg-purple-50 rounded-lg p-4">
				<h3 class="text-sm font-medium text-purple-800 mb-1">Platforms</h3>
				<p class="text-2xl font-bold text-purple-600">${state.results.length}</p>
			</div>
		`;
	}
}

async function loadSavedResults() {
	try {
		const saved = await loadResults();
		if (saved.length > 0) {
			state.results = saved;
			displayResults();
			updateUI();
		}
	} catch (error) {
		console.error("Failed to load saved results:", error);
	}
}

async function clearAll() {
	if (!confirm("Clear all data?")) return;

	state.urls = [];
	state.scrapedData = [];
	state.results = [];

	await clearResults();

	getElement<HTMLDivElement>("progress-container").classList.add("hidden");
	getElement<HTMLDivElement>("results-container").classList.add("hidden");
	getElement<HTMLButtonElement>("analyze-btn").disabled = true;

	const urlList = getElement<HTMLDivElement>("url-list");
	urlList.innerHTML = `
		<div class="url-input-group flex gap-2">
			<input
				type="url"
				class="url-input flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
				placeholder="https://example.com/docs"
				required
			/>
		</div>
	`;
}

function exportMarkdownHandler() {
	if (state.results.length === 0) {
		alert("No results to export. Please analyze documentation first.");
		return;
	}
	exportMarkdown(state.results);
}

function exportCSVHandler() {
	if (state.results.length === 0) {
		alert("No results to export. Please analyze documentation first.");
		return;
	}
	exportCSV(state.results);
}

function updateUI() {
	const scrapeBtn = getElement<HTMLButtonElement>("scrape-btn");
	const analyzeBtn = getElement<HTMLButtonElement>("analyze-btn");
	const exportMdBtn = getElement<HTMLButtonElement>("export-md-btn");
	const exportCsvBtn = getElement<HTMLButtonElement>("export-csv-btn");

	scrapeBtn.disabled = state.isScraping || state.isAnalyzing;
	analyzeBtn.disabled =
		state.isScraping || state.isAnalyzing || state.scrapedData.length === 0;
	exportMdBtn.disabled = state.results.length === 0;
	exportCsvBtn.disabled = state.results.length === 0;

	scrapeBtn.textContent = state.isScraping
		? "Scraping..."
		: "Scrape Documentation";
	analyzeBtn.textContent = state.isAnalyzing ? "Analyzing..." : "Analyze";
}

if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", init);
} else {
	init();
}
