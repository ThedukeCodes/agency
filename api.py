import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in selection]

        return jsonify({
            'success': True,
            'movies': movies,
            'totalMovies': len(Movie.query.all())
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        
        if movie is None:
            abort(404)

        try:
            movie.delete()
            selection = Movie.query.order_by(Movie.id).all()
            movies = [movie.format() for movie in selection]

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': movies,
                'totalMovies': len(Movie.query.all())
            })

        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            movie = Movie(
                title=title,
                release_date=release_date,
                )

            movie.insert()
            selection = Movie.query.order_by(Movie.id).all()
            movies = [movie.format() for movie in selection]

            return jsonify({
                'success': True,
                'created': movie.id,
                'movies': movies,
                'totalMovies': len(Movie.query.all())
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)

            movie.title = title
            movie.release_date = release_date
            selection = Movie.query.order_by(Movie.id).all()
            movies = [movie.format() for movie in selection]

            return jsonify({
                'success': True,
                'updated': movie.id,
                'movies': movies,
                'totalMovies': len(Movie.query.all())
            })

        except:
            abort(422)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in selection]

        return jsonify({
            'success': True,
            'actors': actors,
            'totalActors': len(Actor.query.all())
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        
        if actor is None:
            abort(404)

        try:
            actor.delete()
            selection = Actor.query.order_by(Actor.id).all()
            actors = [actor.format() for actor in selection]

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': actors,
                'totalActors': len(Actor.query.all())
            })

        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            actor = Actor(
                name=name,
                age=age,
                gender=gender
                )

            actor.insert()
            selection = Actor.query.order_by(Actor.id).all()
            actors = [actor.format() for actor in selection]

            return jsonify({
                'success': True,
                'created': actor.id,
                'actors': actors,
                'totalActors': len(Actor.query.all())
            })

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)

            actor.name = name
            actor.age = age
            actor.gender = gender

            selection = Actor.query.order_by(Actor.id).all()
            actors = [actor.format() for actor in selection]

            return jsonify({
                'success': True,
                'updated': actor.id,
                'actors': actors,
                'totalActors': len(Actor.query.all())
            })

        except:
            abort(422)

    return app