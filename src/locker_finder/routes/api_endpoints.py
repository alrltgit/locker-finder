from flask import Blueprint, request, jsonify, render_template
from ..services.inpost_client import InPostClient
from ..services.lockers_search import find_nearest_lockers

bp = Blueprint("lockers", __name__)

@bp.route("/")
def display_map():
    return render_template("index.html")

@bp.route("/api/lockers/nearest")
def get_nearest_lockers():
    lat = request.args.get("lat")
    print(lat)
    lon = request.args.get("lon")
    print(lon)

    if lat is None or lon is None:
        return jsonify({"error": "lat and lon are required"}), 400

    try:
        user_lat = float(lat)
        user_lon = float(lon)
    except ValueError:
        return jsonify({"error": "lat and lon must be numbers"}), 400

    client = InPostClient()
    lockers = client.get_lockers_data(user_lat, user_lon)
    nearest_lockers = find_nearest_lockers(lockers, user_lon, user_lat)

    return jsonify(nearest_lockers)
