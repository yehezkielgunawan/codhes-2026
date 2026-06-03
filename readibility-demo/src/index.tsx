import { Hono } from "hono";
import { ProgressBar } from "./components/ProgressBar";
import { ResultsTable } from "./components/ResultsTable";
import { UrlForm } from "./components/UrlForm";
import { renderer } from "./renderer";
import api from "./routes/api";

const app = new Hono();

app.use(renderer);
app.route("/api", api);

app.get("/", (c) => {
	return c.render(
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

			<UrlForm />
			<ProgressBar />
			<ResultsTable />
		</div>,
	);
});

export default app;
