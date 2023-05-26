import React from "react";
import {useForm} from "react-hook-form";
import {moviesApi} from "@/services/moviesApi.js";
import {useQuery, useQueryClient} from "@tanstack/react-query";
import {Movie} from "@components/movie/Movie.jsx";
import {ClusterData} from "@components/cluster-data/ClusterData.jsx";
import {HashLoader} from "react-spinners";

export const Api = ({apiVersion}) => {
    const {register, handleSubmit} = useForm();
    const movieName = React.useRef("");

    const {
        data: {movies, clusterData} = {}, isFetching, isError, refetch,
    } = useQuery({
        queryKey: [`api${apiVersion}Movies`],
        queryFn: async ({signal}) => {
            return await moviesApi.getMovies(apiVersion, movieName.current, signal);
        },
        enabled: false,
    });

    const queryClient = useQueryClient()

    const onSubmit = (data) => {
        queryClient.cancelQueries({ queryKey: [`api${apiVersion}Movies`] })
        movieName.current = data.movie;
        refetch();
    };

    // justify-content align-items
    return (
        <div className="basis-1/2 flex flex-col gap-5 p-10">
            <div className="flex flex-col justify-start items-stretch gap-3">
                <h1 className="text-5xl font-semibold text-center">
                    API {apiVersion.toUpperCase()}
                </h1>
                <form
                    onSubmit={handleSubmit(onSubmit)}
                    className="flex flex-col align-stretch justify-center gap-5"
                >
                    <input
                        className="flex-1 p-5 rounded border-2 border-gray-400/50 bg-transparent"
                        placeholder={`Search a movie in API ${apiVersion.toUpperCase()}`}
                        {...register("movie")}
                    />
                </form>
            </div>
            {!!movies && !isFetching &&
                <>
                    <h1 className="text-3xl font-bold">Response Information</h1>
                    <ClusterData clusterData={clusterData}/>
                    <h1 className="text-3xl font-bold">Movies</h1>
                    <div className="grid grid-cols-2 gap-4">
                        {movies.map((movie) =>
                            <Movie key={movie.id} movie={movie}/>
                        )}
                    </div>
                </>
            }
            {isFetching &&
                <div className="flex flex-row justify-center items-center h-48">
                    <HashLoader color="#36d7b7"/>
                </div>
            }
        </div>)
};
