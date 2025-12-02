from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship(
        "Movie", backref="user", lazy="select", cascade="all, delete-orphan"
    )  # movie.user to get "owner"


class Movie(db.Model):
    m_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    poster = db.Column(db.String(300), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
