import axios from 'axios';
import {UserAdd} from "../interfaces/IUser.ts";
import {createApi} from "./middleware.ts";


const userApi = createApi('/user');

export const loginUser = async (user: UserAdd) => {
    try {
        const response = await userApi.post('/login', user);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail || 'Login failed');
        }
        throw new Error('Network error');
    }
};

export const createUser = async (user: UserAdd) => {
    try {
        const response = await userApi.post('/register', user);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail || 'User creation failed');
        }
        throw new Error('Network error');
    }
};
