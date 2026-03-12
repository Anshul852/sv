import express, { type Express } from "express";
import cors from "cors";
import { createProxyMiddleware } from "http-proxy-middleware";

const app: Express = express();

app.use(cors({ origin: "*" }));

// Proxy all requests to the Python FastAPI backend
app.use(
  createProxyMiddleware({
    target: "http://localhost:8000",
    changeOrigin: true,
    on: {
      error: (_err, _req, res: any) => {
        res.status(502).json({ error: "Backend unavailable. Python API server may be starting up." });
      }
    }
  })
);

export default app;
