from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@database-service/db'
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
    title = request.args.get('title')
    size = request.args.get('size', default=10, type=int)
    if not title:
        return jsonify({'error': 'Missing title parameter'}), 400

    movies = Movies.query.filter(or_(*[Movies.name.ilike('%{}%'.format(token)) for token in title.split()])).all()

    movies = movies[:size]

    schema = MoviesSchema(many=True)
    serialized_movies = schema.dump(movies)

    return serialized_movies, 200

@app.route('/', methods=['GET'])
def get_api_specification():
    specs = {
        "movies_url": "http://api.movies.com/v1/movies?title={title}{&size}",
    }
    return specs, 200

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
