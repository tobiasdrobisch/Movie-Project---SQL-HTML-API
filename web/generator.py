def generate_html(movies: list[dict]) -> str:
    """Generate the full HTML for the movie website."""

    if not isinstance(movies, list):
        raise TypeError(f"'movies' must be a list, got {type(movies).__name__}")

    try:
        with open("web/index_template.html", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("Template file 'web/index_template.html' not found.")

    movie_grid_html = create_movie_grid(movies)

    html = template.replace("__TEMPLATE_TITLE__", "Movie Collection")
    html = html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)
    html = html.replace("__TEMPLATE_CSS_PATH__", "web/style.css")

    return html


def create_movie_grid(movies: list[dict]) -> str:
    """Return HTML <li> elements for each movie."""

    if not isinstance(movies, list):
        raise TypeError(f"'movies' must be a list, got {type(movies).__name__}")

    movie_items = []

    for m in movies:
        if not isinstance(m, dict):
            raise TypeError(f"Each movie must be a dict, got {type(m).__name__}")

        # Ensure required keys exist
        required = ["poster", "title", "year"]
        for key in required:
            if key not in m:
                raise KeyError(f"Movie entry missing required key: '{key}'")

        movie_items.append(
            f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{m['poster']}" alt="{m['title']}"/>
                    <div class="movie-title">{m['title']}</div>
                    <div class="movie-year">{m['year']}</div>
                </div>
            </li>
            """.strip()
        )

    return "\n".join(movie_items)
