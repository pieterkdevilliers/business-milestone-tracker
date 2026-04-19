export const useApi = () => {
  const config = useRuntimeConfig()
  // SSR: use internal Docker network URL (fast, no round-trip through tunnel)
  // Browser: use public Cloudflare tunnel URL
  const baseUrl = import.meta.server
    ? (config.apiBase as string)
    : config.public.apiBase

  const get = <T>(path: string): Promise<T> =>
    $fetch<T>(`${baseUrl}${path}`)

  const post = <T>(path: string, body: unknown): Promise<T> =>
    $fetch<T>(`${baseUrl}${path}`, { method: "POST", body })

  const patch = <T>(path: string, body: unknown): Promise<T> =>
    $fetch<T>(`${baseUrl}${path}`, { method: "PATCH", body })

  const del = (path: string): Promise<void> =>
    $fetch(`${baseUrl}${path}`, { method: "DELETE" })

  return { get, post, patch, del }
}
