from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@database/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artists = db.Column(db.String(513))
    album_name = db.Column(db.String(243))
    track_name = db.Column(db.String(511))
    duration_ms = db.Column(db.Integer)

    def __repr__(self):
        return '<Music %r>' % self.title

class SongsSchema(Schema):
    id = fields.Int(dump_only=True)
    artists = fields.Str(nullable = False)
    album_name = fields.Str(nullable = True)
    track_name = fields.Str(nullable = True)
    duration_ms = fields.Int(nullable = False)

@app.route('/songs', methods=['GET'])
def get_movies():
    title = request.args.get('title')
    size = request.args.get('size', default=10, type=int)
    if not title:
        return jsonify({'error': 'Missing title parameter'}), 400

    songs = Songs.query.filter(or_(*[Songs.track_name.ilike('%{}%'.format(token)) for token in title.split()])).all()

    songs = songs[:size]

    schema = SongsSchema(many=True)
    serialized_movies = schema.dump(songs)

    return serialized_movies, 200

@app.route('/', methods=['GET'])
def get_api_specification():
    specs = {
        "songs_url": "http://api.songs.com/songs?title={title}{&size}",
    }
    return specs, 200

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
