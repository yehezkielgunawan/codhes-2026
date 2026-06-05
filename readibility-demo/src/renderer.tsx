import { jsxRenderer } from "hono/jsx-renderer";
import { Link, ViteClient } from "vite-ssr-components/hono";

export const renderer = jsxRenderer(({ children }) => {
	return (
		<html lang="en">
			<head>
				<meta charset="UTF-8" />
				<meta name="viewport" content="width=device-width, initial-scale=1.0" />
				<meta name="theme-color" content="#4f46e5" />
				<meta
					name="description"
					content="Compare HTML documentation vs llms.txt files for readability and token efficiency."
				/>
				<title>Readability & Token Efficiency Analyzer</title>
				<link rel="icon" href="/favicon.ico" sizes="any" />
				<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
				<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
				<link rel="manifest" href="/manifest.json" />
				<ViteClient />
				<Link href="/src/style.css" rel="stylesheet" />
			</head>
			<body class="bg-gray-50 text-gray-900 min-h-screen">
				<main class="container mx-auto px-4 py-8 max-w-6xl">{children}</main>
				<script type="module" src="/src/client/app.ts" />
			</body>
		</html>
	);
});
