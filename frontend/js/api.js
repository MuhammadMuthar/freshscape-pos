// FreshScape Market POS -- API client
// Thin fetch wrapper: attaches the auth token, handles 401s by
// bouncing to login, and surfaces backend error messages as toasts.

const API_BASE_URL = 'http://127.0.0.1:8000';
const TOKEN_KEY = 'freshscape_token';

const auth = {
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },
  clearToken() {
    localStorage.removeItem(TOKEN_KEY);
  },
  isLoggedIn() {
    return !!auth.getToken();
  },
  requireAuth() {
    if (!auth.isLoggedIn()) {
      window.location.href = pathToRoot() + 'login.html';
    }
  },
  logout() {
    auth.clearToken();
    window.location.href = pathToRoot() + 'login.html';
  },
};

// Pages under /pages/ need "../login.html"; root pages need "login.html".
function pathToRoot() {
  return window.location.pathname.includes('/pages/') ? '../' : '';
}

async function apiRequest(method, path, body) {
  const headers = {};
  const token = auth.getToken();

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const options = { method, headers };

  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(body);
  }

  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, options);
  } catch (err) {
    throw new Error(
      'Could not reach the server. Is the backend running on ' +
      API_BASE_URL + '?'
    );
  }

  if (response.status === 401) {
    auth.clearToken();
    window.location.href = pathToRoot() + 'login.html';
    // Stop the caller's .then chain from running with no data.
    return new Promise(() => {});
  }

  if (response.status === 204) {
    return null;
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const message = (data && data.detail) || `Request failed (${response.status}).`;
    throw new Error(typeof message === 'string' ? message : JSON.stringify(message));
  }

  return data;
}

const api = {
  get: (path) => apiRequest('GET', path),
  post: (path, body) => apiRequest('POST', path, body ?? {}),
  patch: (path, body) => apiRequest('PATCH', path, body ?? {}),
  delete: (path) => apiRequest('DELETE', path),

  async login(username, password) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params,
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error((data && data.detail) || 'Login failed.');
    }

    return data;
  },
};

// --- Toasts ---

function ensureToastStack() {
  let stack = document.querySelector('.toast-stack');
  if (!stack) {
    stack = document.createElement('div');
    stack.className = 'toast-stack';
    document.body.appendChild(stack);
  }
  return stack;
}

function toast(message, type = 'error') {
  const stack = ensureToastStack();
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.textContent = message;
  stack.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}
