from flask import Blueprint, request, jsonify, render_template

from ..repository.locker_repository import LockerRepository
from ..services.lockers_search import LockerSearch
from ..db.database import get_session

bp = Blueprint("lockers", __name__)

@bp.route("/")
def display_map():
    return render_template("index.html")

@bp.route("/api/lockers/nearest")
def get_nearest_lockers():
    user_lat = request.args.get("lat")
    user_lon = request.args.get("lon")

    if user_lat is None or user_lon is None:
        return jsonify({"error": "lat and lon are required"}), 400

    with get_session() as session:
        repository = LockerRepository(session)
        locker_search = LockerSearch(repository)

        nearest_lockers = locker_search.find_nearest_lockers(float(user_lon), float(user_lat))
    return jsonify([ locker.model_dump() for locker in nearest_lockers ])
