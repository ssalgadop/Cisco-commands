import axios from 'axios'
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/settings/',
});
export const getAllSettings = () => api.get('/');
export const createSetting = (setting) => api.post('/',setting);
