from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import requests
import os
from dotenv import load_dotenv

#load env-variables
load_dotenv()

DB_URL = "sqlite:///db/movies.db"
API_KEY = os.getenv("OMDB_API_KEY")   # <-- holt den Key aus .env

if not API_KEY:
    raise RuntimeError("OMDB_API_KEY is missing in .env")

OMDB_URL = "http://www.omdbapi.com/"

engine = create_engine(DB_URL, echo=False)

# Create table if not exists
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL
        )
    """))
    conn.commit()


def get_movies():
    """Return a list of movie dicts from the database."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT title, year, rating, poster FROM movies"))
        return [dict(row._mapping) for row in result.fetchall()]


def list_movies():
    """Return movies as a title-indexed dictionary."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT title, year, rating FROM movies"))
        return {row[0]: {"year": row[1], "rating": row[2]} for row in result}


def add_movie(title):
    """Fetch and insert a movie by title using OMDb API."""
    data = get_movie_data_by_title(title)

    title = data["Title"]
    year = int(data["Year"])
    rating = float(data["imdbRating"])
    poster = data["Poster"]

    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO movies (title, year, rating, poster)
                VALUES (:title, :year, :rating, :poster)
            """), {"title": title, "year": year, "rating": rating, "poster": poster})
            conn.commit()
    except SQLAlchemyError as error:
        if "UNIQUE constraint failed" in str(error):
            raise FileExistsError(f"Movie '{title}' already exists in the database.")
        raise RuntimeError(f"Database error while adding movie '{title}': {error}")


def delete_movie(title):
    """Delete a movie by title."""
    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        conn.commit()

        if result.rowcount == 0:
            raise KeyError(f"Cannot delete '{title}': movie does not exist.")


def update_movie(title, rating):
    """Update the rating of a movie by title."""
    with engine.connect() as conn:
        result = conn.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
            {"title": title, "rating": rating}
        )
        conn.commit()

        if result.rowcount == 0:
            raise KeyError(f"Cannot update '{title}': movie does not exist.")


def get_movie_data_by_title(title):
    """Retrieve movie data from OMDb by title."""
    response = requests.get(OMDB_URL, params={"apikey": API_KEY, "t": title})

    if response.status_code != 200:
        raise ConnectionError(f"OMDb request failed: {response.status_code}")

    data = response.json()

    if data.get("Response") == "False":
        raise LookupError(f"Movie '{title}' not found in OMDb API.")

    return data
