import axios from 'axios';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para adicionar token automaticamente
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Interceptor para tratar respostas
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token) {
    if (token) {
      this.api.defaults.headers.Authorization = `Bearer ${token}`;
    } else {
      delete this.api.defaults.headers.Authorization;
    }
  }

  // Auth endpoints
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    return this.api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  }

  async refreshToken() {
    return this.api.post('/auth/refresh_token');
  }

  // User endpoints
  async createUser(username, email, password) {
    return this.api.post('/users/', {
      username,
      email,
      password,
    });
  }

  async getUsers(offset = 0, limit = 10) {
    return this.api.get(`/users/?offset=${offset}&limit=${limit}`);
  }

  async getUserById(userId) {
    return this.api.get(`/users/${userId}/`);
  }

  async updateUser(userId, username, email, password) {
    return this.api.put(`/users/${userId}/`, {
      username,
      email,
      password,
    });
  }

  async deleteUser(userId) {
    return this.api.delete(`/users/${userId}/`);
  }

  // Root endpoint
  async getRoot() {
    return this.api.get('/');
  }
}

export const apiService = new ApiService();