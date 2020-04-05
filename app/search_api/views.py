from flask import jsonify
from flask import request
from app.search_api.search_data import PerformVerdict
from . import search_api

AUTH_KEY = "1234ABCD"


@search_api.route("/area-search/", methods=["GET", "POST"])
def view():

    # auth
    headers = request.headers
    auth = headers.get("X-Api-Key")

    # Auth
    if auth != AUTH_KEY:
        return jsonify({"error": "unauthorized"}), 200

    content = request.get_json()
    
    if not list(content.keys()) == ["query"]:
        return jsonify(
            {
                "error": "Query is not properly formatted.",
                "excpectedFormat": "{'query': 'query string'}",
            }
        )

    else:
        try:
            query = content["query"]
            obj = PerformVerdict(query)
            d = obj.verdict()
            d["query"] = query
            return jsonify(d), 200

        except KeyError:
            d = {"mathcedArea": [], "verdictArea": None, "verdictAreaId": None}
            return jsonify(d)
