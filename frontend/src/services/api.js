import axios from "axios";

// VITE_API_URL is baked in at BUILD TIME (Vite requirement -- client-side
// env vars must be prefixed VITE_ and are resolved when `npm run build`
// runs, not at server runtime). Falls back to localhost for local dev
// when no .env is present.
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
});

API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default API;