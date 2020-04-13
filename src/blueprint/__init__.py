from typing import Callable, Optional

from flask import Blueprint


def _factory(
    partial_module_string: str,
    url_prefix: str,
    protected: bool = False,
    auth_function: Optional[Callable] = None,
) -> Blueprint:
    # Create the blueprint
    blueprint = Blueprint(
        partial_module_string,
        f"src.blueprint.{partial_module_string}",
        url_prefix=url_prefix,
    )

    # This endpoint is not to be publicly used
    if protected:
        # Protected endpoints must have an authorization method
        if auth_function is None:
            raise NotImplementedError(
                "An authorization method must be given for protected endpoints!"  # noqa
            )

        # Protect the endpoint with an authorization routine
        blueprint.before_request(auth_function)
    return blueprint


bp_root = _factory("root", "")
bp_admin = _factory("admin", "/admin")
bp_search = _factory("search", "/search")
bp_shortcuts = _factory("shortcuts", "")

all_blueprints = (bp_root, bp_search, bp_shortcuts)
