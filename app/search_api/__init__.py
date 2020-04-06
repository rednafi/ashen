from flask import Blueprint

search_api = Blueprint(
    "search_api", __name__, template_folder="templates", static_folder="static"
)

from . import views  # isort:skip
