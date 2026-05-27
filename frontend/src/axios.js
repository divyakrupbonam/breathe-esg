import axios from "axios";

const api = axios.create({
    baseURL: "https://breathe-esg-production-d49f.up.railway.app",
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

export default api;