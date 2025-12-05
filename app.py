from flask import Flask, redirect, request, url_for, render_template, flash
import os
from dotenv import load_dotenv
from data_manager import DataManager
from models import db, User
import requests

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # Holt  Key
OMDB_BASE_URL = "http://www.omdbapi.com/"

#  Flask App
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dein_geheimer_schlüssel")


#  Basisverzeichnis + DB
basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, "data")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "movies.db")

#  Config muss vor db.init_app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
data_manager = DataManager()

with app.app_context():
    db.create_all()


@app.errorhandler(404)
def pageNotFound(error):
    return "page not found", 404


@app.errorhandler(500)
def Error(error):
    return "Server Error", 500


# home zeigt alle User + Button zum hinzufügen
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        data_manager.create_user(name)
    users =  data_manager.get_all_users()
    return render_template("index.html", users=users)


@app.route("/users/<int:user_id>/movies", methods=["GET", "POST"])
def user_movies(user_id):
    #POST
    if request.method == "POST":
        title = request.form.get("title")
        year_input = request.form.get("year")

        if not title:
            return redirect(url_for("user_movies", user_id=user_id))

        # OMDb API
        params = {"t": title, "apikey": OMDB_API_KEY}
        if year_input and year_input.isdigit():
            params["y"] = year_input

        response = requests.get(OMDB_BASE_URL, params=params)
        data = response.json()

        if data.get("Response") == "False":
             flash(f"Error while fetching: {data.get('Error')}. Or search parameters were incorrect"), 404
             return redirect(url_for("user_movies", user_id=user_id))

        year = data.get("Year")
        director = data.get("Director", "")
        rating = (
            float(data.get("imdbRating"))
            if data.get("imdbRating") != "N/A"
            else None
        )
        poster = data.get("Poster")
        if poster in [None, "N/A"]:
            poster = None

        data_manager.create_movie(
            title=data.get("Title", title),
            publication_year=year,
            director=director,
            rating=rating,
            user_id=user_id,
            poster=poster,
        )
        return redirect(url_for("user_movies", user_id=user_id))

    # GET
    user = data_manager.get_user(user_id)
    if not user:
        return "User not found", 404
    movies = data_manager.get_user_movies(user_id)
    for i in movies:
        print(i.rating)
    return render_template("movies.html", movies=movies, user=user)


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    title = request.form.get("title")
    rating = request.form.get("rating")

    new_rating = None
    if rating and rating.replace(".", "", 1).isdigit():
        new_rating = float(rating)

    try:
        data_manager.update_movie(
            movie_id=movie_id, new_title=title, new_rating=new_rating
        )
    except ValueError as ve:
        return str(ve), 400
    except Exception as e:
        return f"Error updating movie: {e}", 500

    return redirect(url_for("user_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_title(user_id, movie_id):
    movie_to_delete = data_manager.delete_movie(movie_id)
    if not movie_to_delete:
        return "Movie not found or Error deleting", 404
    return redirect(url_for("user_movies", user_id=user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
