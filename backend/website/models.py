from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    preference = db.Column(db.String(150))
    watchlist = db.relationship('Watchlist')
    watched = db.relationship('Watched')
    review = db.relationship('Review', primaryjoin="User.id==Review.user_id")
    vote = db.relationship('Vote')

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    genre = db.Column(db.String(150))
    description = db.Column(db.String(500))
    director = db.Column(db.String(150))
    actors = db.Column(db.String(150))
    year = db.Column(db.Integer)
    runtime = db.Column(db.Integer)
    rating = db.Column(db.Float)
    votes = db.Column(db.Integer)
    image_path = db.Column(db.String(150))
    five_stars = db.Column(db.Integer)
    four_stars = db.Column(db.Integer)
    three_stars = db.Column(db.Integer)
    two_stars = db.Column(db.Integer)
    one_star = db.Column(db.Integer)
    watchlist = db.relationship('Watchlist')
    watched = db.relationship('Watched')
    review = db.relationship('Review')
    vote = db.relationship('Vote')

class Watchlist(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)

class Watched(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    username = db.Column(db.String(150), db.ForeignKey('user.username'))
    rating = db.Column(db.Float)
    comment = db.Column(db.String(800))
    likes = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    vote = db.relationship('Vote')

class Vote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), primary_key=True)
    vote = db.Column(db.Integer)