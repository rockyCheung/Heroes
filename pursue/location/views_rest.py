from operator import and_

from flask import Blueprint
from flask import jsonify
from flask import g
from flask import request
from werkzeug.exceptions import abort
from pursue import db
from pursue.user.views import login_required
import logging
import json
from  pursue.utils.alchemy_to_json import alchemy_to_json
from pursue.location.models import Location

bp = Blueprint("location", __name__ ,url_prefix="/api/v1.0/location")


def creatLocation():
    location = Location()
    location.user_id = g.user.id
    location.coordinate = request.json.get('coordinate')
    location.altitude = request.json.get('altitude')
    location.speed = request.json.get('speed')
    location.course = request.json.get('course')

    return location

@bp.route("/<string:created>", methods=["GET"])
@login_required
def query_starttime(created):
    logging.debug('@created:%s', created)
    if created is not None:
        location = Location.query.filter(Location.created>=created,Location.user_id==g.user.id).all()

    return json.dumps(location, cls=alchemy_to_json(), check_circular=False)

@bp.route("/<string:starttime>/<string:endtime>", methods=["GET"])
@login_required
def query_betwentime(starttime,endtime):
    logging.debug('@starttime:%s', starttime)
    if starttime is not None:
        location = Location.query.filter(Location.created>=starttime,Location.created<=endtime,Location.user_id==g.user.id).all()
    return json.dumps(location, cls=alchemy_to_json(), check_circular=False)

@bp.route("/", methods=["GET"])
@login_required
def query_all():
    location = Location.query.filter(Location.user_id==g.user.id).all()
    return json.dumps(location, cls=alchemy_to_json(), check_circular=False)


@bp.route("/", methods=["POST"])
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        location = creatLocation()
        db.session.add(location)
        db.session.commit()
        return jsonify({'result':'successed'})

    return jsonify({'result':'failed'})
