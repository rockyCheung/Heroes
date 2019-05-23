import os

import click
from flask import Flask
from flask import request
from flask.cli import with_appcontext
from flask.logging import default_handler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

__version__ = (1, 0, 0, "dev")


logging.basicConfig(filename='pursue.log',level=logging.DEBUG)
db = SQLAlchemy()

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.logger.removeHandler(default_handler)

    migrate = Migrate(app, db)
    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        # default to a sqlite database in the instance folder
        db_url = "sqlite:///" + os.path.join(app.instance_path, "pursue.sqlite")
        # ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    # apply the blueprints to the app
    from pursue import user, blog, blackbox, location
    #rest api views define to bp,page for bp
    app.register_blueprint(user.bpp)
    app.register_blueprint(blog.bpp)
    app.register_blueprint(blackbox.bp)
    app.register_blueprint(location.bp)
    app.register_blueprint(location.bpp)

    # make "index" point at "/", which is handled by "blog.index"
    app.add_url_rule("/", endpoint="index")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        app.logger.info("per request commit this")
        pass

    return app


def init_db():
    db.drop_all()
    db.create_all()



@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")