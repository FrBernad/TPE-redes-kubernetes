import axios from "axios";

const apiAxios = axios.create();

export const moviesApi = {
    getMovies: async (version, name, signal) => {
        const response = await apiAxios.get(`http://api.movies.com:5000/${version}/movies`, {
            params: {
                name,
            },
            signal,
        });

        return {
            clusterData: {
                podIP: response.headers['x-pod-ip'],
                podName: response.headers['x-pod-name'],
                node: response.headers['x-node-name'],
            }, movies: response.data,
        }
    },
};