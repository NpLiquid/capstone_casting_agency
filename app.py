import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, db_drop_and_create_all, setup_db, Movie, Actor, Assignation
from auth import AuthError, requires_auth

def prepopulate_db():
  data_present = Movie.query.all()

  if len(data_present) == 0:
    try:
      movie1 = Movie(title='Rogue One A Star Wars Story', release_date='13 December 2016')
      movie1.insert()
      movie2 = Movie(title='Full Speed Ahead', release_date='13 September 1951')
      movie2.insert()
      movie3 = Movie(title='Rebel Without a Cause', release_date='20 January 1956')
      movie3.insert()
      movie4 = Movie(title='The Human Contract', release_date='20 January 2021')
      movie4.insert()

      actor1 = Actor(name='James Dean', age= 24, gender='male')
      actor1.insert()
      actor2 = Actor(name='Felicity Jones', age= 36, gender='female')
      actor2.insert()
      actor3 = Actor(name='Pedro Infante', age= 38, gender='male')
      actor3.insert()
      actor4 = Actor(name='Paz Vega', age= 44, gender='female')
      actor4.insert()

      assign1 = Assignation(movie_id=1, actor_id=2)
      assign1.insert()
      assign2 = Assignation(movie_id=2, actor_id=3)
      assign2.insert()
      assign3 = Assignation(movie_id=3, actor_id=1)
      assign3.insert()
    except:
      print('Error when populating the database')

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  migrate = Migrate(app,setup_db)

  # cleans the database and populate it if needed
  # make sure to comment the db_drop_and_create_all function before run the test_app.py
  #--------------------------------------#
  #db_drop_and_create_all()
  prepopulate_db()


  #----------------------------------------------------------------------------#
  # Controllers.
  #----------------------------------------------------------------------------#
  @app.route('/')
  def welcome():
    return 'Welcome to the Casting Agency "Films Udacity" API\n'

  #----------------------------------------------------------------------------#
  #  Movies
  #----------------------------------------------------------------------------#
  # Query
  #--------------------------------------#
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    movies_list = Movie.query.order_by(Movie.id).all()

    data = []
    for m in movies_list:
      cast_data = []
      try:
        cast_list = Assignation.query.filter(Assignation.movie_id == m.id).all()
        if len(cast_list) > 0:
          for c in cast_list:
            actor = Actor.query.filter(Actor.id == c.actor_id).first()
            cast_data.append(actor.name)
      except():
        error = True
      data.append({
        "id": m.id,
        "title": m.title,
        "release_date": m.release_date,
        "cast": cast_data
      })
    
    return jsonify({
      'success': True,
      'movie': data
    }), 200

  # Delete
  #--------------------------------------#
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
    movie = Movie.query.get(id)
      
    if movie is None:
        abort(404)
    
    try:
      movie.delete()

      return jsonify({
        'success': True,
        'movie': movie.format()
      }),200
    except:
      abort(422)

  # Create
  #--------------------------------------#
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movie(payload):
    body = request.get_json()

    new_title = body.get('title')
    new_release_date = body.get('release_date')

    if new_title == '' or new_release_date == '':
      abort(422)
    
    try:
      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()
      
      return jsonify({
        'success': True,
        'movie': movie.format()
      }),200
    except:
      abort(422)

  # Update
  #--------------------------------------#
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movie(payload, id):
    movie = Movie.query.get(id)
    if movie is None:
      abort(404)

    body = request.get_json()
    if 'title' in body:
      movie.title = body['title']

    if 'release_date' in body:
      movie.release_date = body['release_date']

    movie.update()

    return jsonify({
        'success': True,
        'movie': movie.format()
    }),200

  #----------------------------------------------------------------------------#
  #  Actors
  #----------------------------------------------------------------------------#
  # Query
  #--------------------------------------#
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    actors_list = Actor.query.order_by(Actor.id).all()
    data = []
    for a in actors_list:
      films_data = []
      try:
        films_list = Assignation.query.filter(Assignation.actor_id == a.id).all()
        if len(films_list) > 0:
          for f in films_list:
            movie = Movie.query.filter(Movie.id == f.movie_id).first()
            films_data.append(movie.title)
      except():
        error = True
      
      data.append({
        "id": a.id,
        "name": a.name,
        "age": a.age,
        "gender": a.gender,
        "filmography": films_data
      })
    
    return jsonify({
      'success': True,
      'actor': data
    }), 200

  # Delete
  #--------------------------------------#
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload,id):
    actor = Actor.query.get(id)
      
    if actor is None:
        abort(404)
    
    try:
      actor.delete()

      return jsonify({
        'success': True,
        'actor': actor.format()
      }),200
    except:
      abort(422)

  # Create
  #--------------------------------------#
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actor(payload):
    body = request.get_json()

    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')

    if new_name == '' or new_age == '' or new_gender == '':
      abort(422)
    
    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()
      
      return jsonify({
        'success': True,
        'actor': actor.format()
      }),200
    except:
      abort(422)

  # Update
  #--------------------------------------#
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(payload, id):
    actor = Actor.query.get(id)
    if actor is None:
      abort(404)

    body = request.get_json()
    if 'name' in body:
      actor.name = body['name']

    if 'age' in body:
      actor.age = body['age']

    if 'gender' in body:
      actor.gender = body['gender']

    actor.update()

    return jsonify({
        'success': True,
        'actor': actor.format()
    }),200

  #----------------------------------------------------------------------------#
  #  Assignations
  #----------------------------------------------------------------------------#

  #----------------------------------------------------------------------------#
  #  Error Handling
  #----------------------------------------------------------------------------#
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  @app.errorhandler(401)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": "unauthorized"
    }), 401

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      "success": False,
      "error": error.status_code,
      "message": error.error['description']
    }), error.status_code

  return app

APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)