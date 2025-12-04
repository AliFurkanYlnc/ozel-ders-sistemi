import client from './client';
import { User } from '../store/authStore';

export type AuthResponse = {
  token: string;
  user: User;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type RegisterPayload = {
  email: string;
  password: string;
  role: User['role'];
};

export const login = async (data: LoginPayload): Promise<AuthResponse> => {
  const response = await client.post<AuthResponse>('/auth/login', data);
  return response.data;
};

export const register = async (data: RegisterPayload): Promise<AuthResponse> => {
  const response = await client.post<AuthResponse>('/auth/register', data);
  return response.data;
};

export const getMe = async (): Promise<User> => {
  const response = await client.get<User>('/auth/me');
  return response.data;
};
