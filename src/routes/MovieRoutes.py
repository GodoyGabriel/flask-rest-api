from flask import Blueprint, jsonify, request
import uuid
from models.MovieModel import MovieModel
from models.entities.Movie import Movie

main = Blueprint('movie_blueprint', __name__)


@main.route('/', methods=['GET'])
def get_movies():
    try:
        movies = MovieModel.get_movies()
        return jsonify(movies)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<id>', methods=['GET'])
def get_movie(id):
    try:
        movie = MovieModel.get_movie(id)
        if movie != None:
            return jsonify(movie)
        return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_movie():
    try:
        title = request.json['title']
        duration = int(request.json['duration'])
        released = request.json['released']
        id = str(uuid.uuid4())
        movie = Movie(id, title, duration, released)
        affected_rows = MovieModel.add_movie(movie)
        if affected_rows == 1:
            return jsonify(movie.id)
        return jsonify({'message': 'Error on insert'}), 500
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<id>', methods=['PUT'])
def update_movie(id):
    try:
        title = request.json['title']
        duration = int(request.json['duration'])
        released = request.json['released']
        movie = Movie(id, title, duration, released)
        affected_rows = MovieModel.update_movie(movie)
        if affected_rows == 1:
            return jsonify(movie.id)
        return jsonify({'message': 'No movie updated'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/delete/<id>', methods=['DELETE'])
def delete_movie(id):
    try:
        affected_rows = MovieModel.delete_movie(id)
        if affected_rows == 1:
            return jsonify(id)
        return jsonify({'message': 'No movie deleted'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
