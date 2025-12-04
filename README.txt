# Movie WebApp

A simple web application to manage movies. Users can add, view, and update movies. External movie data comes from the [OMDb API](http://www.omdbapi.com/).

## Features
- User management
- Add, view, and edit movies
- Rating (1–10)
- Optional title field when updating
- External movie info from OMDb API

## Installation
1. Clone the repository:
   ```bash
   git clone <REPO_URL>
   cd MovieWebApp
2.Create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows

3. Install dependencies
    pip install -r requirements.txt

4. Set OMDb API key in .env file
    OMDB_API_KEY=your_api_key

### Uusage
1. start Flask
    flask run

2. open browser
     http://127.0.0.1:5000

3. Search, add, view, and update movies.


####Structure

app.py – Flask routes

data_manager.py – Database operations

templates/ – HTML templates

static/ – CSS, JS, images

OMDb API – External movie info via API key
