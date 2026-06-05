export function ResultsTable() {
	return (
		<div
			id="results-container"
			class="hidden bg-white rounded-lg shadow-md p-6"
		>
			<h2 class="text-xl font-semibold mb-4 text-gray-800">Analysis Results</h2>

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
					<tbody id="results-body">{/* Filled by client JS */}</tbody>
				</table>
			</div>

			<div
				id="summary-cards"
				class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6"
			>
				{/* Filled by client JS */}
			</div>

			<div class="flex gap-3 mt-6">
				<button
					type="button"
					id="export-md-btn"
					class="px-4 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition disabled:opacity-50"
					disabled
				>
					Export Markdown
				</button>
				<button
					type="button"
					id="export-csv-btn"
					class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-500 transition disabled:opacity-50"
					disabled
				>
					Export CSV
				</button>
			</div>
		</div>
	);
}
