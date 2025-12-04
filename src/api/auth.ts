import client from './client';

export type User = {
  id: string;
  email: string;
  role: 'student' | 'tutor';
  [key: string]: any;
};

export async function login(params: { email: string; password: string }): Promise<{ user: User; token: string }> {
  const response = await client.post('/auth/login', params);
  const { access_token, user } = response.data;
  return { user, token: access_token };
}

export async function register(params: {
  email: string;
  password: string;
  role: 'student' | 'tutor';
}): Promise<{ user: User; token: string }> {
  await client.post('/auth/register', params);
  return login({ email: params.email, password: params.password });
}
