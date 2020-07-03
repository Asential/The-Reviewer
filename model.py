import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column('id',db.Integer, primary_key=True)
    name = db.Column('Name',db.String, nullable=True)
    password = db.Column('Password',db.String, nullable=True)
    email = db.Column('E-Mail',db.String, nullable=True)

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column('id', db.Integer, primary_key=True)
    isbn = db.Column('isbn', db.String, nullable=True)
    title = db.Column('title', db.String, nullable=True)
    author = db.Column('author', db.String, nullable=True)
    year = db.Column('year', db.Integer, nullable=True)

class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column('id', db.Integer, primary_key=True)
    isbn = db.Column('isbn', db.String, nullable=True)
    review = db.Column('review', db.String, nullable=True) 
    rating = db.Column('rating', db.Integer, nullable=True)
    name = db.Column('name', db.String, nullable=True)

# Function for the animated star rating system
def r(strs):
    if strs == 'star-4':
        return 5
    if strs == 'star-3':
        return 4
    if strs == 'star-2':
        return 3
    if strs == 'star-1':
        return 2
    if strs == 'star-0':
        return 1


