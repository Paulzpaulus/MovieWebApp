from flask import Flask
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)

# Basis-Verzeichnis ermitteln
basedir = os.path.abspath(os.path.dirname(__file__))

# create "data"
db_dir = os.path.join(basedir, "data")
os.makedirs(db_dir, exist_ok=True)

# Path
db_path = os.path.join(db_dir, "movies.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app
data_manager = DataManager()  # Create an object of your DataManager class

@app.route("/")
def home():
    return "Welcome to MovieWeb App!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
