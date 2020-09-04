import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from flask_moment import Moment

database_name = "casting_agency"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movies
'''
class Movie(db.Model):  
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(120),nullable = False)
  release_date = Column(String(120),nullable = False)
  cast = db.relationship('Assignation', backref='Movie', passive_deletes=True, lazy=True)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }

'''
Actors
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(120),nullable = False)
  age = Column(Integer, nullable=False)
  gender = Column(String(120),nullable = False)
  filmography = db.relationship('Assignation', backref='Actor', passive_deletes=True, lazy=True)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }

'''
Assignations
'''
class Assignation(db.Model):  
  __tablename__ = 'Assignation'

  id = Column(Integer, primary_key=True, autoincrement=True)
  movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id', ondelete='CASCADE'),nullable=False)
  actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id', ondelete='CASCADE'),nullable=False)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'movie_id': self.movie_id,
      'actor_id': self.actor_id,
    }