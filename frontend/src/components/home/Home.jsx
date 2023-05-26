import React from "react";
import {Api} from "@components/api/Api.jsx";

export const Home = () => {
    return (
        <main className="flex flex-1 flex-col">
            <div className="flex h-44 justify-center items-center">
                <h1 className="text-6xl font-bold text-center">Movies API</h1>
            </div>
            <div className="flex flex-row">
                <Api apiVersion="v1"/>
                <Api apiVersion="v2"/>
            </div>
        </main>
    );
};
