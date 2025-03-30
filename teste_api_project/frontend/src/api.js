import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Substitua pela URL do backend, se necessário
});

export default api;
