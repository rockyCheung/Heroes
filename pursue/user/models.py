from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from pursue import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    status = db.Column(db.Integer, unique=False, server_default='1')
    createdtime = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    # privatekey = db.Column(db.String, unique=False, nullable=False )
    mail = db.Column(db.String, unique=False, nullable=True)
    mobile = db.Column(db.String, unique=False, nullable=True)
    qq = db.Column(db.String, unique=False, nullable=True)
    address = db.Column(db.String, unique=False, nullable=True)
    career = db.Column(db.String, unique=False, nullable=True)
    sex = db.Column(db.String, unique=False, nullable=True)
    age = db.Column(db.Integer, unique=False, nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Store the password as a hash for security."""
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    # @hybrid_property
    # def privatekey(self):
    #     return self.privatekey
