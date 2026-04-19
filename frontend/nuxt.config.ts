export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: false },
  devServer: { host: "0.0.0.0" },
  modules: ["@pinia/nuxt", "@nuxtjs/tailwindcss"],
  runtimeConfig: {
    // Server-side only — used during SSR via Docker network
    apiBase: process.env.NUXT_API_BASE || "http://backend:8000",
    public: {
      // Exposed to the browser — must be the public tunnel URL in prod
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },
});
