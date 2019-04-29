from pursue import db
from pursue.user.models import User



class Accountbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    account = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    siteurl = db.Column(db.String, nullable=True)
    decription = db.Column(db.String, nullable=True)
