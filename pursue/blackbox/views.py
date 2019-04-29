from flask import Blueprint
from flask import flash,jsonify
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from pursue import db
from pursue.user.views import login_required
from pursue.blackbox.models import Accountbox
import logging
import json
from  pursue.utils.alchemy_to_json import alchemy_to_json

bp = Blueprint("blackbox", __name__ ,url_prefix="/api/v1.0/blackbox")


def get_accountbox(id):
    accountbox = db.session.query(Accountbox).get(id)
    logging.debug('@@@accountbox %s',accountbox.account)
    return accountbox

def creatAccountbox(accountbox):
    accountbox.user_id = g.user.id
    account = request.json.get('account')
    password = request.json.get('password')
    accountbox.siteurl = request.json.get('siteurl')
    accountbox.decription = request.json.get('decription')
    error = None

    if not account or not password:
        error = "Account and password is required."

    if error is not None:
        flash(error)
        
    else:
        logging.debug("creatAccountbox privatekey: %s", g.user.privatekey)
        # aes = pyaes.AESModeOfOperationCTR(base64.decodebytes(g.user.privatekey))
        logging.debug("creatAccountbox the account : %s password: % s",account,password)
        accountbox.password = password
        accountbox.account = account
        logging.debug("creatAccountbox encrypt after the account : %s password: % s", accountbox.account, accountbox.password)
    return error,accountbox

@bp.route("/<string:decription>", methods=["GET"])
@login_required
def query(decription):
    logging.debug('@decription:%s',decription)
    if decription is not None:
        accountbox = Accountbox.query.filter(Accountbox.decription.like('%'+decription+'%')).all()
    else :
        accountbox = Accountbox.query.order_by(Accountbox.created.desc()).all()
    alchemylist = []
    resultbox = []
    # aes = pyaes.AESModeOfOperationCTR(base64.decodebytes(g.user.privatekey))
    if isinstance(accountbox,Accountbox):
        alchemylist.append(accountbox)
    else:
        alchemylist = accountbox

    for box in alchemylist:
        resultbox.append(box)
    
    return json.dumps(resultbox, cls=alchemy_to_json(), check_circular=False)

@bp.route("/", methods=["GET"])
@login_required
def query_all():
    return query(decription=None)

@bp.route("/", methods=["POST"])
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        error,accountbox = creatAccountbox(Accountbox())
        db.session.add(accountbox)
        db.session.commit()
        return jsonify({'result':'successed'})

    return jsonify({'result':'failed'})


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def update(id):
    """Update a post if the current user is the author."""
    accountbox = Accountbox()#get_accountbox(id)
    accountbox.id = id
    if request.method == "PUT":
        account = request.json.get('account')
        password = request.json.get('password')
        siteurl = request.json.get('siteurl')
        decription = request.json.get('decription')
        if account is not None:
            accountbox.account = account
        if password is not None:
            accountbox.password = password
        if siteurl is not None:
            accountbox.siteurl = siteurl
        if decription is not None:
            accountbox.decription = decription
            
        db.session.merge(accountbox)
        db.session.commit()
        return jsonify({'result':'successed'})

    return jsonify({'result':'failed'})


@bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete(id):
    """Delete a accountbox.

    Ensures that the accountbox exists.
    """
    accountbox = get_accountbox(id)
    db.session.delete(accountbox)
    db.session.commit()
    return redirect(url_for("blog.index"))
