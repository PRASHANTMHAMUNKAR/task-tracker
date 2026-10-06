import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    // Local dev only: forward /api to the Flask backend
    proxy: { "/api": "http://localhost:5000" },
  },
});
