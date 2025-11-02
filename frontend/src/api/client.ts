import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({ 
  baseURL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur pour les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export async function get<T>(url: string) {
  try {
    const { data } = await api.get<T>(url)
    return data
  } catch (error: any) {
    console.error('GET Error:', error)
    throw error
  }
}

export async function post<T>(url: string, body?: unknown, config?: any) {
  try {
    const { data } = await api.post<T>(url, body, config)
    return data
  } catch (error: any) {
    console.error('POST Error:', error)
    throw error
  }
}


