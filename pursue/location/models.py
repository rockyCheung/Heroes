from flask import url_for
from pursue import db
from pursue.user.models import User

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    coordinate = db.Column(db.String, nullable=False) # 当前位置所在的经、纬度数据
    altitude = db.Column(db.String, nullable=False) #海拔
    speed = db.Column(db.String, nullable=False) #当前速度
    course = db.Column(db.String, nullable=False) #航向(设备的移动方向,值域范围0.0~359.9,正北方向为0.0)
    user = db.relationship(User, lazy="joined", backref="locations")