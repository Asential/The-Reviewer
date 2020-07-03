import sqlite3
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model import User, Books   

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Searches by string input
def search_results(sq):
    search_query = sq.lower() 
    courses = db.execute("SELECT * FROM books WHERE LOWER(isbn) LIKE :search_query OR LOWER(title) LIKE :search_query OR LOWER(author) LIKE :search_query OR year LIKE :search_query", {"search_query": "%" + search_query + "%"}).fetchall()
    return courses

# Searches only by ISBN
def search_isbn(sq):
    search_query = sq.lower() 
    courses = db.execute("SELECT * FROM books WHERE isbn LIKE :search_query", {"search_query": search_query}).first()
    return courses