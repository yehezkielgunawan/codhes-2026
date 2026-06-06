import { useState } from "hono/jsx";

interface BulkUrlInputProps {
	onUrlsParsed: (urls: string[]) => void;
}

function parseUrlsFromText(text: string): string[] {
	const lines = text.split("\n").map((line) => line.trim());
	const urls: string[] = [];

	for (const line of lines) {
		if (!line) continue;

		const urlMatch = line.match(/https?:\/\/[^\s\)]+/);
		if (urlMatch) {
			urls.push(urlMatch[0]);
		}
	}

	return urls;
}

export function BulkUrlInput({ onUrlsParsed }: BulkUrlInputProps) {
	const [text, setText] = useState("");
	const [parsedCount, setParsedCount] = useState(0);

	const handleTextChange = (e: Event) => {
		const value = (e.target as HTMLTextAreaElement).value;
		setText(value);
		const urls = parseUrlsFromText(value);
		setParsedCount(urls.length);
	};

	const handleParse = () => {
		const urls = parseUrlsFromText(text);
		if (urls.length === 0) {
			alert("No URLs found in the text");
			return;
		}
		if (urls.length > 10) {
			alert(
				`Found ${urls.length} URLs, but maximum is 10. Only the first 10 will be used.`,
			);
			onUrlsParsed(urls.slice(0, 10));
		} else {
			onUrlsParsed(urls);
		}
	};

	return (
		<div class="bg-white rounded-lg shadow-md p-6 mb-6">
			<h2 class="text-xl font-semibold mb-4 text-gray-800">Bulk URL Input</h2>
			<p class="text-sm text-gray-600 mb-4">
				Paste your URL list below. URLs will be extracted automatically from
				formats like:
				<br />
				<code class="text-xs bg-gray-100 px-1 py-0.5 rounded">
					1. React JS (https://react.dev/)
				</code>
				<br />
				<code class="text-xs bg-gray-100 px-1 py-0.5 rounded">
					https://example.com/docs
				</code>
			</p>

			<textarea
				class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
				rows={10}
				placeholder="Paste your URL list here..."
				value={text}
				onInput={handleTextChange}
			/>

			<div class="mt-3 flex items-center justify-between">
				<p class="text-sm text-gray-600">
					{parsedCount > 0
						? `${parsedCount} URL${parsedCount !== 1 ? "s" : ""} detected`
						: "No URLs detected yet"}
				</p>
				<button
					type="button"
					class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition disabled:opacity-50"
					disabled={parsedCount === 0}
					onClick={handleParse}
				>
					Use These URLs
				</button>
			</div>
		</div>
	);
}
