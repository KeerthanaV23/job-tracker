import axios from "axios";

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "/api" });

const getTokens = () => JSON.parse(localStorage.getItem("tokens") || "null");
export const saveTokens = (t) => localStorage.setItem("tokens", JSON.stringify(t));
export const clearTokens = () => localStorage.removeItem("tokens");

api.interceptors.request.use((config) => {
  const t = getTokens();
  if (t?.access) config.headers.Authorization = `Bearer ${t.access}`;
  return config;
});

// Auto-refresh the access token once on 401
let refreshing = null;
api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    const t = getTokens();
    if (error.response?.status === 401 && t?.refresh && !original._retry && !original.url.includes("/auth/")) {
      original._retry = true;
      try {
        refreshing = refreshing || axios.post(`${api.defaults.baseURL}/auth/refresh/`, { refresh: t.refresh });
        const { data } = await refreshing;
        refreshing = null;
        saveTokens({ ...t, access: data.access });
        original.headers.Authorization = `Bearer ${data.access}`;
        return api(original);
      } catch (e) {
        refreshing = null;
        clearTokens();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export const errorMessage = (err) => {
  const d = err.response?.data;
  if (!d) return "Something went wrong. Try again.";
  if (typeof d === "string") return d;
  if (d.detail) return d.detail;
  return Object.entries(d).map(([k, v]) => `${k}: ${[].concat(v).join(" ")}`).join(" | ");
};

export default api;
