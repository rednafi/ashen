from flask import jsonify
from flask import request
from app.search_api.search_data import PerformVerdict
from . import search_api

AUTH_KEY = "1234ABCD"


@search_api.route("/area-search/", methods=["GET"])
def get_main_func():

    # auth
    headers = request.headers
    auth = headers.get("X-Api-Key")

    # Auth
    if auth != AUTH_KEY:
        return jsonify({"error": "unauthorized"}), 200

    try:
        query = request.args["q"]
        obj = PerformVerdict(query)
        d = obj.verdict()
        return jsonify(d), 200

    except KeyError:
        d = {"mathcedArea": [], "verdictArea": None, "verdictAreaId": None}
        return jsonify(d), 400

    except Exception:
        d = {"mathcedArea": [], "verdictArea": None, "verdictAreaId": None}
        return jsonify(d)
