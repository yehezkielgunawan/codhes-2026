import { Hono } from "hono";
import { renderer } from "./renderer";

const app = new Hono();

app.use(renderer);

app.get("/", (c) => {
	return c.render(
		<div class="text-center">
			<h1 class="text-4xl font-bold text-blue-600 mb-4">Hello!</h1>
			<p class="text-lg text-gray-600">
				Welcome to the Readibility Demo built with Hono + Tailwind CSS.
			</p>
		</div>,
	);
});

export default app;
