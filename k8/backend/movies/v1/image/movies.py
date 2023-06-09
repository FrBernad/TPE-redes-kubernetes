from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from marshmallow import Schema, fields
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, expose_headers='*')

database_user = os.environ["POSTGRES_USER"]
database_password = os.environ["POSTGRES_PASS"]
database_db = os.environ["POSTGRES_DB"]
database_host = os.environ["POSTGRES_HOST"]

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database_user}:{database_password}@{database_host}/{database_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return '<Movie %r>' % self.name

class MoviesSchema(Schema):
    id = fields.Int(dump_only=True)
    year = fields.Int()
    name = fields.Str(required=True)
    director = fields.Str()

@app.route('/movies', methods=['GET'])
def get_movies():
    name = request.args.get('name')
    size = request.args.get('size', default=5, type=int)

    if not name:
        response = jsonify({'error': 'Missing name parameter'})
        response.status_code = 400
        response.headers.extend(_get_response_headers())
        return response

    movies = Movies.query.filter(or_(*[Movies.name.ilike('%{}%'.format(token)) for token in name.split()])).all()

    movies = movies[:size]

    schema = MoviesSchema(many=True)
    serialized_movies = schema.dump(movies)

    response = make_response(serialized_movies, 200)
    response.headers.extend(_get_response_headers())
    
    return response

@app.route('/', methods=['GET'])
def get_api_specification():
    specs = {
        "movies_url": "http://api.movies.com/v1/movies?name={name}{&size}",
    }

    response = make_response(specs, 200)

    response.headers.extend(_get_response_headers())

    return response

def _get_response_headers():
    return {
        'X-POD-IP': os.environ.get('POD_IP'),
        'X-POD-NAME': os.environ.get('POD_NAME'),
        'X-NODE-NAME': os.environ.get('NODE_NAME'),
    }

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
