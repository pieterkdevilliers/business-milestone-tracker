export const useApi = () => {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBase

  const get = <T>(path: string): Promise<T> =>
    $fetch<T>(`${baseUrl}${path}`)

  const patch = <T>(path: string, body: unknown): Promise<T> =>
    $fetch<T>(`${baseUrl}${path}`, { method: "PATCH", body })

  return { get, patch }
}
