/*
  Simple JWT auth helper for frontend
  - Obtains token pair from /api/token/
  - Stores tokens in localStorage (you may choose cookies for better security)
  - Automatically refreshes access token when expired using /api/token/refresh/
  - Provides authenticatedFetch wrapper

  Usage example:
    import { login, logout, authFetch, getAccessToken } from './api-auth.js'

    await login('user@example.com', 'password')
    const resp = await authFetch('/api/results/')

  Notes:
  - Adjust API_BASE to match your backend host/port.
  - For production prefer HttpOnly secure cookies instead of localStorage.
*/

const API_BASE = window.API_BASE || '' // e.g. 'http://127.0.0.1:8000'
const TOKEN_KEY = 'mylab_tokens' // stores {access, refresh, access_expires_at}

function nowSeconds() {
    return Math.floor(Date.now() / 1000)
}

function saveTokens(tokens) {
    // tokens: { access, refresh }
    const payload = { access: tokens.access, refresh: tokens.refresh }
    try {
        // try to decode access JWT exp
        const parts = tokens.access.split('.')
        if (parts.length === 3) {
            const payloadRaw = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'))
            const data = JSON.parse(decodeURIComponent(escape(payloadRaw)))
            if (data && data.exp) payload.access_expires_at = data.exp
        }
    } catch (e) {
        // ignore decode errors
    }
    localStorage.setItem(TOKEN_KEY, JSON.stringify(payload))
}

function loadTokens() {
    const raw = localStorage.getItem(TOKEN_KEY)
    if (!raw) return null
    try { return JSON.parse(raw) } catch (e) { return null }
}

export async function login(username, password) {
    const res = await fetch(`${API_BASE}/api/auth/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Login failed' }))
        throw err
    }
    const data = await res.json()
    saveTokens({ access: data.access, refresh: data.refresh })
    return data
}

export async function register(payload) {
    // payload: { username, email, password, password2, first_name?, last_name?, role?, phone? }
    const res = await fetch(`${API_BASE}/api/accounts/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Register failed' }))
        throw err
    }
    const data = await res.json()
    // response expected to include access & refresh
    if (data.access && data.refresh) saveTokens({ access: data.access, refresh: data.refresh })
    return data
}

export function logout() {
    localStorage.removeItem(TOKEN_KEY)
}

export function getAccessToken() {
    const t = loadTokens()
    return t ? t.access : null
}

async function refreshAccessToken() {
    const t = loadTokens()
    if (!t || !t.refresh) return null
    const res = await fetch(`${API_BASE}/api/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: t.refresh })
    })
    if (!res.ok) {
        logout()
        return null
    }
    const data = await res.json()
    saveTokens({ access: data.access, refresh: t.refresh })
    return data.access
}

async function ensureAccessToken() {
    const t = loadTokens()
    if (!t) return null
    if (t.access_expires_at && (t.access_expires_at - 30) > nowSeconds()) {
        return t.access
    }
    // otherwise, refresh
    return await refreshAccessToken()
}

// Wrapper around fetch which ensures Authorization header
export async function authFetch(input, init = {}) {
    let token = await ensureAccessToken()
    if (!token) throw new Error('Not authenticated')
    init.headers = init.headers || {}
    init.headers['Authorization'] = `Bearer ${token}`
    // default JSON accept
    if (!init.headers['Accept']) init.headers['Accept'] = 'application/json'
    return fetch(input.startsWith('http') ? input : (API_BASE + input), init)
}

// Helper to check login state
export function isLoggedIn() {
    return !!getAccessToken()
}

// Expose default export for legacy script tags
const apiAuthDefault = { login, logout, authFetch, getAccessToken, isLoggedIn }

// Expose default export for module consumers
export default apiAuthDefault

// Also expose a global `Auth` for legacy/non-module pages
try {
    if (typeof window !== 'undefined') {
        if (!window.API_BASE) window.API_BASE = ''
        window.Auth = apiAuthDefault
    }
} catch (e) {
    // ignore in non-browser environments
}
