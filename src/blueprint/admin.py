from flask import abort

from src.blueprint import admin


@admin.route("/")
def index():
    abort(404)


@admin.route("/config")
def config():
    abort(404)


@admin.route("/prompts/edit/<string:prompt_date>")
def prompt_edit(prompt_date: str):
    abort(404)


@admin.route("/writers")
def writers():
    abort(404)


@admin.route("/writers/edit/<int:writer_id>")
def writer_edit(writer_id: int):
    abort(404)
