import { Hono } from "hono";
import { renderer } from "./renderer";
import api from "./routes/api";

const app = new Hono();

app.use(renderer);
app.route("/api", api);

app.get("/", (c) => {
	return c.render(<div id="root" />);
});

export default app;
