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


@admin.route("/hosts")
def hosts():
    abort(404)


@admin.route("/hosts/edit/<int:host_id>")
def host_edit(host_id: int):
    abort(404)
