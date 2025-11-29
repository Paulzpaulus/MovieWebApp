from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)



class Movie(db.Model):
    m_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    publication_year = db.Column(db.Integer, nullable = False)
    director = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.Float, nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
