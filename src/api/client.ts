import axios from 'axios';
import useAuthStore from '../store/authStore';

const client = axios.create({
  baseURL: 'http://localhost:5000',
});

client.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    // eslint-disable-next-line no-param-reassign
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

export default client;
