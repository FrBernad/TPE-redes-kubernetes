import React from "react";

export const ClusterData = ({clusterData}) => {
    return (<div className="glass p-5">
        <div className="flex flex-col">
            <p className="text-xl"><span className="font-bold">Node: </span>{clusterData.node}</p>
            <p className="text-xl"><span className="font-bold">Pod: </span>{clusterData.podName}</p>
            <p className="text-xl"><span className="font-bold">Pod IP: </span>{clusterData.podIP}</p>
        </div>
    </div>);
};
