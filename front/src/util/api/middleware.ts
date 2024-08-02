import axios from 'axios';
import useAuthStore from "../storage/authStore.ts";

function createApi(route: string) {
    const api = axios.create({
        baseURL: 'http://localhost:8000/' + route,
        headers: {
            'Content-Type': 'application/json',
        },
    });

    api.interceptors.response.use(
        (response) => {
            const auth_header = response.headers['Authorization'];
            if (auth_header) {
                const newToken = auth_header.replace('Bearer ', '');
                useAuthStore.getState().setToken(newToken);
            }
            return response;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    return api;
}

export {createApi};
