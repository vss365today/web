from pathlib import Path

from flask import redirect, render_template, url_for

from src.blueprints import stats


def get_years() -> list[int]:
    """Get all available statistics years."""
    path = (Path() / "src" / "templates" / "stats" / "years").resolve()
    return [int(f.stem) for f in path.iterdir()]


@stats.get("/")
def index():
    render_opts = {"years": get_years()}
    return render_template("stats/index.html", **render_opts)


@stats.get("/<int:year>")
def year(year: int):
    return f"stats/{year}"
    render_opts = {}

    return render_template("root/index.html", **render_opts)
    return redirect(url_for("stats.index"))
