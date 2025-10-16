def generate_html(movies: list[dict]) -> str:
    """Generate the full HTML for the movie website."""
    with open("web/index_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    movie_grid_html = create_movie_grid(movies)
    html = template.replace("__TEMPLATE_TITLE__", "Movie Collection")
    html = html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)
    html = html.replace("__TEMPLATE_CSS_PATH__", "web/style.css")

    return html


def create_movie_grid(movies: list[dict]) -> str:
    """Return HTML <li> elements for each movie."""
    return "\n".join(
        f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{m['poster']}" alt="{m['title']}"/>
                <div class="movie-title">{m['title']}</div>
                <div class="movie-year">{m['year']}</div>
            </div>
        </li>
        """.strip()
        for m in movies
    )
