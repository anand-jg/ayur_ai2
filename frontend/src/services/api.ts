import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    withCredentials: true,
});

export const auth = {
    login: async (username: string, password: string) => {
        const response = await api.post('/auth/users/login/', { username, password });
        return response.data;
    },
    register: async (userData: {
        username: string;
        email: string;
        password: string;
        first_name: string;
        last_name: string;
        role: string;
        phone_number: string;
    }) => {
        const response = await api.post('/auth/users/register/', userData);
        return response.data;
    },
    logout: async () => {
        const response = await api.post('/auth/users/logout/');
        return response.data;
    },
};

export const decisions = {
    getQuestions: async () => {
        const response = await api.get('/decisions/questions/');
        return response.data;
    },
    submitResponse: async (responseData: {
        question: number;
        answer: number;
        session_id: string;
    }) => {
        const response = await api.post('/decisions/responses/', responseData);
        return response.data;
    },
    getDiagnosis: async (sessionId: string) => {
        const response = await api.get(`/decisions/diagnoses/?session_id=${sessionId}`);
        return response.data;
    },
};

export const recommendations = {
    getDoctors: async (params?: {
        specialization?: string;
        location?: string;
        min_rating?: number;
        max_fee?: number;
    }) => {
        const response = await api.get('/recommendations/doctors/', { params });
        return response.data;
    },
    bookAppointment: async (appointmentData: {
        doctor: number;
        date: string;
        time: string;
        notes?: string;
    }) => {
        const response = await api.post('/recommendations/appointments/', appointmentData);
        return response.data;
    },
    submitReview: async (reviewData: {
        doctor: number;
        rating: number;
        comment?: string;
    }) => {
        const response = await api.post('/recommendations/reviews/', reviewData);
        return response.data;
    },
};

export const ai = {
    getDecisionPoints: async () => {
        const response = await api.get('/ai/decision-points/');
        return response.data;
    },
    getPrompts: async () => {
        const response = await api.get('/ai/prompts/');
        return response.data;
    },
    getResponses: async () => {
        const response = await api.get('/ai/responses/');
        return response.data;
    },
};

export default api; 