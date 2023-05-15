from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@database/movies_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    director = db.Column(db.String(255))
    year = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    genre =   db.Column(db.String(60), nullable=False)
    score  =  db.Column(db.NUMERIC)
    director = db.Column(db.String(150), nullable=True)
    writer   = db.Column(db.String(150), nullable=True)
    star     = db.Column(db.String(150), nullable=True)
    company  = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<Movie %r>' % self.title

@app.route('/movies', methods=['GET'])
def get_movies():
    title = request.args.get('title')
    size = request.args.get('size', default=10, type=int)
    if not title:
        return jsonify({'error': 'Missing title parameter'}), 400

    movies = Movies.query.filter(or_(*[Movies.name.ilike('%{}%'.format(token)) for token in title.split()])).all()

    movies = movies[:size]

    movies_json = [{'name': movie.name} for movie in movies]

    return jsonify(movies_json), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
