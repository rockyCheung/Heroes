# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g
from pursue.user.views import login_required
from pursue.location.models import Location
from flask import render_template

bpp = Blueprint("location_for_page", __name__ ,url_prefix="/location")

@bpp.route("/query", methods=["GET"])
@login_required
def query():
    location = Location.query.filter(Location.user_id==g.user.id).all()
    return render_template("location/index.html", locations=location)