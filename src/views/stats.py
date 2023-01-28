from pathlib import Path

from flask import abort, render_template

from src.blueprints import stats


def get_years() -> list[int]:
    """Get all available statistics years."""
    path = (Path() / "src" / "templates" / "stats" / "years").resolve()
    return [int(f.stem) for f in path.iterdir()]


@stats.get("/")
def index() -> str:
    """Present available years of stats."""
    render_opts = {"years": get_years()}
    return render_template("stats/index.html", **render_opts)


@stats.get("/<int:year>")
def year(year: int) -> str:
    """View a specific year's stats."""
    # Handle not having stats for the requested year
    if year not in get_years():
        abort(404)
    return render_template(f"stats/years/{year}.html")
