const apiUrl = import.meta.env.VITE_API_URL || "/api";

export async function sendRequest<T>(endpoint: string, setState: React.Dispatch<React.SetStateAction<T>> | null = null, method: HttpMethod = methods.GET, body?: any): Promise<T> {
  const res = await fetch(`${apiUrl}` + endpoint, {
    method,
    headers: { "Content-Type": "application/json" },
    ...(body && { body: JSON.stringify(body) }),
  });

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  const data = (await res.json()) as T;

  if (setState != null) {
    setState(data);
  }

  return data
}

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export const methods: Record<HttpMethod, HttpMethod> = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  PATCH: "PATCH",
  DELETE: "DELETE"
};
