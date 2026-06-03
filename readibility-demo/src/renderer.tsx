import { jsxRenderer } from "hono/jsx-renderer";
import { Link, ViteClient } from "vite-ssr-components/hono";

export const renderer = jsxRenderer(({ children }) => {
	return (
		<html lang="en">
			<head>
				<meta charset="UTF-8" />
				<meta name="viewport" content="width=device-width, initial-scale=1.0" />
				<title>Readibility Demo</title>
				<ViteClient />
				<Link href="/src/style.css" rel="stylesheet" />
			</head>
			<body class="bg-gray-50 text-gray-900 min-h-screen">
				<main class="container mx-auto px-4 py-8">{children}</main>
			</body>
		</html>
	);
});
