import React from "react";

export const Movie = ({movie}) => {
    return (<div className="glass p-5">
        <h1 className="text-2xl font-bold">{movie.name}</h1>
        <div className="flex flex-col">
            {movie.genre && <p><span className="font-bold">Genre:</span> {movie.genre}</p>}
            <p><span className="font-bold">Year:</span> {movie.year}</p>
            {movie.score && <p><span className="font-bold">Rating:</span> {movie.score}/10</p>}
            <p><span className="font-bold">Director:</span> {movie.director}</p>
            {movie.writer && <p><span className="font-bold">Writer:</span> {movie.writer}</p>}
        </div>
    </div>);
};
// v2
//     id = db.Column(db.Integer, primary_key=True)
//     year = db.Column(db.Integer)
//     name = db.Column(db.String(200), nullable=False)
//     director = db.Column(db.String(150), nullable=True)
//     genre =   db.Column(db.String(60), nullable=False)
//     score  =  db.Column(db.NUMERIC)
//     writer   = db.Column(db.String(150), nullable=True)
//     star     = db.Column(db.String(150), nullable=True)
//     company  = db.Column(db.String(120), nullable=True)
//     country

// v1
//     id = db.Column(db.Integer, primary_key=True)
//     year = db.Column(db.Integer)
//     name = db.Column(db.String(200), nullable=False)
//     director = db.Column(db.String(150), nullable=True)