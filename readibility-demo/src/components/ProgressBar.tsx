export function ProgressBar() {
	return (
		<div
			id="progress-container"
			class="hidden bg-white rounded-lg shadow-md p-6 mb-6"
		>
			<h3 class="text-lg font-medium mb-3 text-gray-800">Scraping Progress</h3>
			<div class="w-full bg-gray-200 rounded-full h-4 mb-2">
				<div
					id="progress-bar"
					class="bg-blue-600 h-4 rounded-full transition-all duration-300"
					style="width: 0%"
				/>
			</div>
			<p id="progress-text" class="text-sm text-gray-600">
				0 / 0 URLs processed
			</p>
		</div>
	);
}
