export function UrlForm() {
	return (
		<div class="bg-white rounded-lg shadow-md p-6 mb-6">
			<h2 class="text-xl font-semibold mb-4 text-gray-800">
				Documentation URLs
			</h2>
			<p class="text-sm text-gray-600 mb-4">
				Enter up to 10 documentation URLs. We'll automatically detect llms.txt
				files.
			</p>

			<div id="url-list" class="space-y-2 mb-4">
				<div class="url-input-group flex gap-2">
					<input
						type="url"
						class="url-input flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
						placeholder="https://example.com/docs"
						required
					/>
				</div>
			</div>

			<div class="flex gap-2">
				<button
					type="button"
					id="add-url-btn"
					class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
				>
					+ Add URL
				</button>
			</div>

			<div class="mt-6 flex gap-3 flex-wrap">
				<button
					type="button"
					id="scrape-btn"
					class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition disabled:opacity-50"
				>
					Scrape Documentation
				</button>

				<button
					type="button"
					id="analyze-btn"
					class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition disabled:opacity-50"
					disabled
				>
					Analyze
				</button>

				<button
					type="button"
					id="clear-btn"
					class="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
				>
					Clear All
				</button>
			</div>
		</div>
	);
}
