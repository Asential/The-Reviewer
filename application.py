import os

from flask import Flask, session, request, render_template, redirect, url_for, jsonify, g
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy  import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DecimalField, TextAreaField, RadioField
from wtforms.validators import InputRequired, Email, Length
from model import User, Books, Reviews, r
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from api import imp
from search import search_results, search_isbn
from datetime import date


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'Thisisthesecretkey'
app.config['JSON_SORT_KEYS'] = False
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.query(User).get(int(user_id))

# WTForm Classes
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=32)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=32)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=100)])
    
class Search(FlaskForm):
    searchbar = StringField('searchbar')

class Review(FlaskForm):
    star = RadioField('star', validators=[InputRequired(message="Select a Rating!")], choices=[('star-0','1'), ('star-1','2'), ('star-2','3'), ('star-3','4'), ('star-4','5')])
    review = TextAreaField('review', validators=[InputRequired(), Length(min = 10, max = 500, message="Please keep the review between 20 - 500 characters")])

# Global Variables
signedup = False

@app.route("/")
def index():
    global signedup
    signedup = False
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Bool for registration success html
    global signedup

    # Bool for displaying html in case of invalid credentials
    invalidCredentials = False

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = db.query(User).filter_by(name=username).first()
        
        # user = db.execute('SELECT * FROM ' +  '"Users" ' +  'WHERE ' + '"Name" ' + 'LIKE :user', {"user": "%" + username + "%"}).first() 
        # I couldn't get this command to work with login_manager'
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                signedup = False
                return redirect(url_for('home'))

        signedup = False
        invalidCredentials = True
        return render_template('login.html', form=form, signedup = signedup, invalidCredentials = invalidCredentials)
    print("invalid")
    return render_template('login.html', form=form, signedup = signedup, invalidCredentials = invalidCredentials)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    global signedup
    signedup = False
    invalidCredentials = False

    if request.method == 'POST' and form.validate_on_submit():
    
        name = form.username.data
        email = form.email.data
        password = form.password.data

        # Converting the string password to hash
        hashed_password = generate_password_hash(password, method='sha256')

        # Making a User Class object
        newUser = User(name=name, email=email, password=hashed_password)

        # Adding and commiting the new user
        db.add(newUser)
        db.commit()
        signedup = True
        return redirect(url_for('login'))

    elif request.method == 'POST':
        invalidCredentials = True

    return render_template('register.html', form=form, invalidCredentials = invalidCredentials)

@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    form = Search()

    # Bool for no search results
    notfound = True

    if  request.method == 'POST' and form.validate_on_submit():
        
        search_query = form.searchbar.data

        # Search function from search.py
        results = search_results(search_query)
        if results:
            notfound = False
            return render_template("search.html", result = results, username = current_user.name, found = notfound)
        else:
            return render_template("search.html", result = results, username = current_user.name, found = notfound)

    return render_template("books.html", username = current_user.name, form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template("home.html", username = current_user.name)

@app.route('/profile')
@login_required
def profile():

    # Bool for no reviews to display on profile
    none = True

    # Gets the review data by matching the name of the current user to the name on reviews
    review_data = db.execute("SELECT * FROM reviews WHERE name LIKE :user ORDER BY id DESC", {"user": "%" + current_user.name + "%"}).fetchall()
    
    if review_data:
        none = False
    return render_template("profile.html", username = current_user.name, review_data = review_data, noreview = none)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template("search.html", result = results)

@app.route("/review/<int:book_id>", methods=['GET', 'POST'])
@login_required
def review(book_id):
    form = Review()

    # Gets the book information by matching the ID in URL to Book ID
    book = db.execute("SELECT * FROM books WHERE id = :book_id", {"book_id":  book_id}).first()
    book_isbn = book.isbn

    # Uses the imp function to import GoodReads data
    goodreads_data = imp(book_isbn)
    
    # Gets the current user's name
    user = current_user.name
    
    # Gets the names from all the reviews on the book to compare to the 
    # current user so as to prevent them to submit another review
    review_data_names = db.execute("SELECT name FROM reviews WHERE LOWER(isbn) LIKE :book_isbn", {"book_isbn": "%" + book_isbn.lower() + "%"})
    
    # Gets all the reviews of the book
    review_data = db.execute("SELECT * FROM reviews WHERE LOWER(isbn) LIKE :book_isbn ORDER BY id DESC", {"book_isbn": "%" + book_isbn.lower() + "%"}).fetchall()
    
    today = date.today()

    rating = goodreads_data["books"][0]["average_rating"]
    ID = goodreads_data["books"][0]["id"]
    ratings_count = goodreads_data["books"][0]["ratings_count"]
    reviews_count = goodreads_data["books"][0]["reviews_count"]
    
    if form.validate_on_submit():
        rev = form.review.data
        star = form.star.data
        rate = r(star)

        # Comparing the names on the review
        for name in review_data_names:
            user_name = name.name
            if user_name == current_user.name:
                return render_template("review.html", form = form, username = current_user.name, i = book, rating = rating, ID = ID, rating_count = ratings_count, review_count = reviews_count, review_data = review_data, error = True)
        
        # Creating a new object of Review class
        newReview = Reviews(rating=rate, review=rev, name=current_user.name, isbn = book_isbn)
        
        # Adding and commiting the new review
        db.add(newReview)
        db.commit()

        # Updating review_data
        review_data = db.execute("SELECT * FROM reviews WHERE LOWER(isbn) LIKE :book_isbn", {"book_isbn": "%" + book_isbn.lower() + "%"}).fetchall()
        return render_template("review.html", form = form, username = current_user.name, i = book, rating = rating, ID = ID, rating_count = ratings_count, review_count = reviews_count, review_data = review_data, error = False)

    return render_template("review.html", form = form, username = current_user.name, i = book, rating = rating, ID = ID, rating_count = ratings_count, review_count = reviews_count, review_data = review_data, error = False)

@app.route("/api/<book_isbn>")
def isbn(book_isbn):
    
    # Search function from search.py searching only by ISBN
    result = search_isbn(book_isbn)

    if result:
        review_count = 0
        total_ratings = 0
        review_data = db.execute("SELECT * FROM reviews WHERE LOWER(isbn) LIKE :book_isbn ORDER BY id DESC", {"book_isbn": "%" + book_isbn.lower() + "%"}).fetchall()
        
        # Calculating Average rating and review count
        for i in review_data:
            total_ratings += i.rating
            review_count += 1 
        average_score = total_ratings/review_count

        # Jsonifying and displaying the data
        return  jsonify(title = result.title, author = result.author, year = result.year, isbn = result.isbn, review_count = review_count, average_score = average_score)
    
    else:
        return render_template('404.html')
