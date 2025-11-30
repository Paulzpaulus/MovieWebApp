from models import db, Movie, User

class DataManager():
    """ handles CRUD operations for USER and MOVIE models"""

    def create_user(self, name: str):
        """ creates user and safes it to database"""
        user = User(name=name)
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            print(f"Error:{e}")
            db.session.rollback()

    def get_user(self):
        try:
            users = User.query.all()
            return users
        except Exception as e:
            print(f" Error: {e}")
            return []
    def delete_user(self, user_id: int):
        """
        deletes a user from db
        """
        user = User.query.get(user_id)
        if not user:
            return False
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def create_movie(self, title: str,publication_year: int, director: str, rating: float | None, user_id: int):
        """
        creates and persists a movie
        """
        if not title and not publication_year:
            raise ValueError("title or publication year must not be empty.")
        if not isinstance(publication_year, int):
            raise TypeError("publictaion year must be an integer.")

        movie = Movie(
        title=title,
        publication_year=publication_year,
        director=director,
        rating=rating,
        user_id=user_id
    )
        try:
            db.session.add(movie)
            db.session.commit()
            return movie
        except Exception as e:
            print(f"Error:{e}")
            db.session.rollback()
            raise e



    def get_user_movies(self, user_id: int):
        """
        Returns a list of movies for the given user_id.
        """
        movies = Movie.query.filter_by(user_id=user_id).all()
        if not movies:
            return []
        return movies

    def update_movie(self, movie_id: int, new_rating: float):
        """
        will allow to change the personal rating for a movie
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            return None

        movie.rating = new_rating
        try:
            db.session.commit()
            return movie
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return None


    def delete_movie(self, movie_id: int):
        """
        deletes user from database.
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            return False
        try:
            db.session.delete(movie)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

