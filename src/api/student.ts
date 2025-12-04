import client from './client';

export interface StudentProfilePayload {
  full_name: string;
  grade: '11' | '12' | 'graduate';
  target_exam: 'TYT' | 'AYT' | 'BOTH';
  target_score?: number | null;
  target_rank?: number | null;
  city?: string;
  district?: string;
  neighborhood?: string | null;
  preferred_modes?: string[];
  notes?: string | null;
}

export const getStudentProfile = () => client.get('/students/me');

export const upsertStudentProfile = (payload: StudentProfilePayload) =>
  client.post('/students/me', payload);

export const getMyAvailability = () => client.get('/availability/me');

export const createAvailabilitySlot = (payload: {
  day_of_week: number;
  start_time: string;
  end_time: string;
}) => client.post('/availability', payload);

export const updateAvailabilitySlot = (
  id: number,
  payload: {
    day_of_week?: number;
    start_time?: string;
    end_time?: string;
  },
) => client.put(`/availability/${id}`, payload);

export const deleteAvailabilitySlot = (id: number) =>
  client.delete(`/availability/${id}`);
