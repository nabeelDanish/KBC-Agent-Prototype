import axios from 'axios'

const API = axios.create({ baseURL: "http://4db7-34-67-127-125.ngrok.io" });

export const fetchPosts = () => API.get('/posts');
export const createPost = (newPost) => API.post('/posts', newPost);
export const updatePost = (id, updatedPost) => API.patch(`/posts/${id}`, updatedPost);
export const deletePost = (id) => API.delete(`/posts/${id}`);
export const likePost = (id) => API.patch(`/posts/${id}/likePost`);

export const signin = (formData) => API.post(`/users/signin`, formData);
export const signup = (formData) => API.post(`/users/signup`, formData);

// Used for MUKALMA
export const sendMessage = (message) => API.post('/reply', message)
export const fetchSource = () => API.get('/source')
export const fetchTopics = () => API.get('/topics')
export const changeTopic = (topic) => API.post('/topics/select', topic)
