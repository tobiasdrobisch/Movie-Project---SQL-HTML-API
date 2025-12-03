import random
from core import storage
from web import generator


class MovieDatabase:
    """
    A class to manage a collection of movies, providing methods
    to add, delete, update, search, and analyze movies.
    """

    def __init__(self):
        """Initialize the movie database by loading from storage."""
        self._load_movies()

    def _load_movies(self):
        """Load movies from the storage into self.movies."""
        self.movies = storage.get_movies()

    def list_movies(self):
        """Print all movies with their year and rating."""
        movies = storage.list_movies()
        print(f"{len(movies)} movies in total")
        for title, data in movies.items():
            print(f"{title} ({data['year']}): {data['rating']}")

    def add_movie(self):
        """Prompt for a movie title and add it to the database."""
        self._load_movies()
        title = get_title_input("Enter a movie to add: ")

        if self._find_exact_title(title):
            raise FileExistsError(f"Cannot add '{title}': movie is already listed.")

        storage.add_movie(title)

    def delete_movie(self):
        """Prompt for a movie title and delete it."""
        title = get_title_input("Enter a movie to delete: ")

        if not self._find_exact_title(title):
            raise KeyError(f"Cannot delete '{title}': movie not found.")

        storage.delete_movie(title)

    def update_movie(self):
        """Prompt for a movie and update its rating."""
        title = get_title_input("Enter a movie to update: ")

        if not self._find_exact_title(title):
            raise KeyError(f"Cannot update '{title}': movie not found.")

        try:
            new_rating = float(input("Enter new rating: "))
            if not 0 <= new_rating <= 10:
                raise ValueError("Rating must be between 0 and 10.")
        except ValueError as error:
            raise ValueError(f"Invalid rating input: {error}")

        storage.update_movie(title, new_rating)

    def show_stats(self):
        """Display stats: average, median, best and worst rated movies."""
        self._load_movies()

        if not self.movies:
            raise LookupError("Cannot compute statistics: no movies in database.")

        ratings = sorted([m["rating"] for m in self.movies])
        count = len(ratings)
        avg = sum(ratings) / count

        median = (
            (ratings[count // 2 - 1] + ratings[count // 2]) / 2
            if count % 2 == 0
            else ratings[count // 2]
        )

        best = max(self.movies, key=lambda m: m["rating"])
        worst = min(self.movies, key=lambda m: m["rating"])

        print(f"\nAverage rating: {avg:.2f}")
        print(f"Median rating: {median:.2f}")
        print(f"Best movie: {best['title']} ({best['year']}) - {best['rating']}")
        print(f"Worst movie: {worst['title']} ({worst['year']}) - {worst['rating']}")

    def random_movie(self):
        """Display a random movie from the database."""
        self._load_movies()
        if not self.movies:
            raise LookupError("Cannot pick a random movie: database is empty.")

        movie = random.choice(self.movies)
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    def search_movie(self):
        """Search and display movies by partial title match."""
        self._load_movies()
        term = input("Enter part of movie name: ").strip().lower()

        matches = [m for m in self.movies if term in m["title"].lower()]

        if not matches:
            raise LookupError(f"No movies found containing '{term}'.")

        for movie in matches:
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    def movies_sorted_by_rating(self):
        """List all movies sorted by descending rating."""
        self._load_movies()
        if not self.movies:
            raise LookupError("Cannot sort movies: database is empty.")

        sorted_movies = sorted(self.movies, key=lambda m: m["rating"], reverse=True)
        for movie in sorted_movies:
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    def generate_website(self):
        """Generate a website with the movie list."""
        self._load_movies()

        if not self.movies:
            raise LookupError("Cannot generate website: no movies in database.")

        html = generator.generate_html(self.movies)
        with open("./web/index.html", "w", encoding="utf-8") as f:
            f.write(html)

        print("Website was generated successfully.")

    def _find_exact_title(self, title: str):
        """Return title if exists in movie list (case-insensitive)."""
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                return movie["title"]
        return None


def get_title_input(prompt="") -> str:
    """Prompt user for non-empty title input."""
    while True:
        title = input(prompt).strip()
        if title:
            return title
        print("An empty title is not allowed. Try again.")
