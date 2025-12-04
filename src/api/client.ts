import axios from 'axios';
import useAuthStore from '../store/authStore';

const client = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL || 'http://localhost:5000',
});

client.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

export default client;
