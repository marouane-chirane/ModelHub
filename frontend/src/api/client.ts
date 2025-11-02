import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({ baseURL })

export async function get<T>(url: string) {
  const { data } = await api.get<T>(url)
  return data
}

export async function post<T>(url: string, body?: unknown, config?: any) {
  const { data } = await api.post<T>(url, body, config)
  return data
}


