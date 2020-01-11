from flask import request
from flask import abort, redirect, render_template, url_for

from src.blueprint import admin
from src.core.config import (
    load_json_config,
    save_json_config
)
from src.core.helpers import split_hashtags_into_list


@admin.route("/")
def index():
    abort(404)


@admin.route("/config")
def config():
    render_opts = {
        "json_config": load_json_config()
    }
    return render_template("admin/config.html", **render_opts)


@admin.route("/config/save", methods=["POST"])
def config_save():
    # Get the submitted form data and current config
    form_data = request.form
    current_config = load_json_config()

    # Map the form field names to their config names
    mapping = {
        "input-hashtags-identifier": "identifiers",
        "input-hashtags-filter": "additionals",
        "input-hashtag-posi": "word_index"
    }

    # Map field specific converters to format the data correctly
    converters = {
        "word_index": lambda x: int(x) - 1 if int(x) - 1 >= 0 else 0,
        "identifiers": lambda x: split_hashtags_into_list(x),
        "additionals": lambda x: split_hashtags_into_list(x)
    }

    # Determine which form was submitted and cleanup the data
    found_key = {
        mapping[key]: converters[mapping[key]](value)
        for key, value in form_data.items()
        if key in mapping
    }

    # Update the config with the new value,
    # clobbering whatever value we previously had
    current_config.update(found_key)

    # Save the updated config
    save_json_config(current_config)

    # TODO Some form of "success" message
    return redirect(url_for("admin.config"))


@admin.route("/prompts")
def prompts():
    abort(404)


@admin.route("/prompts/edit/<string:prompt_date>")
def prompt_edit(prompt_date: str):
    abort(404)


@admin.route("/hosts")
def hosts():
    abort(404)


@admin.route("/hosts/edit/<string:host_id>")
def host_edit(host_id: str):
    abort(404)
