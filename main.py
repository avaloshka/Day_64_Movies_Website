from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Create DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create Table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(2500), nullable=True)
    img_url = db.Column(db.String, nullable=False)


db.create_all()


class RateMovieForm(FlaskForm):
    title = StringField('title')
    rating = StringField('rating')
    review = StringField('review')
    submit = SubmitField('Submit')


class FindMovieForm(FlaskForm):
    title = StringField('title')
    submit = SubmitField('submit')


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)


MOVIE_URL = os.environ['MOVIE_URL']
MOVIE_API_KEY = os.environ['MOVIE_API_KEY']
SESSION_ID = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlMzk1ZjE2NTk5MzQ5YjE0YjkzM2U1ZWVkNzYwY2E3OSIsInN1YiI6IjYxNmE4ZjNiNWNlYTE4MDA2Mjc4MjgwNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ckNs3h05UHdjh-gDAcZxajLgPpHams2d7KaBYVRz8XY'


@app.route('/add', methods=["Get", "POST"])
def add():
    form = FindMovieForm()

    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_URL, params={'api_key': MOVIE_API_KEY, 'query': movie_title})
        data = response.json()['results']
        print(data)
        return render_template("select.html", options=data)
    return render_template('add.html', form=form)


@app.route('/find')
def find():
    movie_app_id = request.args.get('id')


@app.route('/delete')
def delete_movie():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.add(movie.rating)
        db.session.add(movie.review)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)


@app.route('/select')
def select():
    return render_template('select.html')


if __name__ == '__main__':
    app.run(debug=True)
