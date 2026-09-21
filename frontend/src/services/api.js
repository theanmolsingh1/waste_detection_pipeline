const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
async function get(path) { const response = await fetch(`${BASE}${path}`); if (!response.ok) throw new Error(await response.text()); return response.json() }
export const api = { health: () => get('/health'), detections: () => get('/detections'), alerts: () => get('/alerts'), statistics: () => get('/statistics'), performance: () => get('/statistics/performance'), streamUrl: `${BASE}/camera/stream` }
