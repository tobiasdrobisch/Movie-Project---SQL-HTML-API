from sqlalchemy import create_engine, text
import requests

DB_URL = "sqlite:///db/movies.db"
API_KEY = "31421472"
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
    try:
        data = get_movie_data_by_title(title)
        title = data["Title"]
        year = int(data["Year"])
        rating = float(data["imdbRating"])
        poster = data["Poster"]

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO movies (title, year, rating, poster)
                VALUES (:title, :year, :rating, :poster)
            """), {"title": title, "year": year, "rating": rating, "poster": poster})
            conn.commit()
            print(f"Movie '{title}' added successfully.")
    except Exception as e:
        print(f"Error adding movie: {e}")


def delete_movie(title):
    """Delete a movie by title."""
    with engine.connect() as conn:
        try:
            conn.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
            conn.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting movie: {e}")


def update_movie(title, rating):
    """Update the rating of a movie by title."""
    with engine.connect() as conn:
        try:
            conn.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": title, "rating": rating}
            )
            conn.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error updating movie: {e}")


def get_movie_data_by_title(title):
    """Retrieve movie data from OMDb by title."""
    response = requests.get(OMDB_URL, params={"apikey": API_KEY, "t": title})
    return response.json()
