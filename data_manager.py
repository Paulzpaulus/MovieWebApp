from models import db, Movie, User


class DataManager:
    """handles CRUD operations for USER and MOVIE models"""

    # USER
    def create_user(self, name: str):
        """creates user and safes it to database"""
        user = User(name=name)
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            print(f"Error:{e}")
            db.session.rollback()

    def get_user(self, user_id):
        """
        returns user by ID
        """
        try:
            return User.query.get(user_id)
        except Exception as e:
            print(f"Error getting User:{e}")
            db.session.rollback()
            return None

    def get_all_users(self):
        """returns all users, if no users or Error return empty list"""
        try:
            users = User.query.all()
            return users
        except Exception as e:
            print(f" Error: {e}")
            db.session.rollback()
            return []

    # for later implementation - not implemented as route or in html yet
    # def delete_user(self, user_id: int):
    #     """
    #     deletes a user from db
    #     """
    #     user = User.query.get(user_id)
    #     if not user:
    #         return False
    #     try:
    #         db.session.delete(user)
    #         db.session.commit()
    #         return True
    #     except Exception as e:
    #         db.session.rollback()
    #         return False

    # Movies
    def create_movie(
        self,
        title: str,
        publication_year: str | None,
        director: str,
        rating: float | None,
        user_id: int,
        poster: str | None,
    ):
        """
        creates and persists a movie
        """
        if not title and not publication_year:
            raise ValueError("title or publication year must not be empty.")
        if not isinstance(publication_year, (str, None)):
            raise TypeError("publictaion year must be an integer.")
        print(rating)
        movie = Movie(
            title=title,
            publication_year=publication_year,
            director=director,
            rating=rating,
            user_id=user_id,
            poster=poster,
        )
        try:
            db.session.add(movie)
            db.session.commit()
            return movie
        except Exception as e:
            print(f"Error:{e}")
            db.session.rollback()
            raise e

    def get_user_movies(self, user_id: int) -> list[Movie]:
        """Returns a list of movies for the given user_id."""
        try:
            return Movie.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error fetching movies: {e}")
            db.session.rollback()
            return []

    def get_movie(self, movie_id):
        try:
            return Movie.query.get(movie_id)
        except Exception as e:
            print(f"Error while fetching movie: {e}")
            return None

    def update_movie(
        self,
        movie_id: int,
        new_title: str | None = None,
        new_rating: float | None = None,
    ):
        """
        Updates the movie's title and/or rating.
        Rating must be between 1 and 10 if provided.
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            return None  # Movie existiert nicht

        if new_title:
            movie.title = new_title

        if new_rating is not None:
            if not (1 <= new_rating <= 10):
                raise ValueError("Rating must be between 1 and 10")
            movie.rating = new_rating

        try:
            db.session.commit()
            return movie
        except Exception as e:
            db.session.rollback()
            print(f"Error updating movie: {e}")
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
