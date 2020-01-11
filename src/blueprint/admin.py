from flask import abort, render_template

from src.blueprint import admin
from src.core.config import load_json_config


@admin.route("/")
def index():
    abort(404)


@admin.route("/config")
def config():
    render_opts = {
        "json_config": load_json_config()
    }
    return render_template("admin/config.html", **render_opts)


@admin.route("/prompts")
def prompts():
    abort(404)


@admin.route("/prompts/edit/<string:prompt_date>")
def prompt_edit(prompt_date: str):
    abort(404)


@admin.route("/hosts")
def hosts():
    abort(404)


@admin.route("/hosts/edit/<str:host_id>")
def host_edit(host_id: str):
    abort(404)
