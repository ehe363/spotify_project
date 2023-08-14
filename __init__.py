import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables or a config file
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SPOTIFY_CLIENT_ID'] = os.getenv("CLIENT_ID")
    app.config['SPOTIFY_CLIENT_SECRET'] = os.getenv("CLIENT_SECRET")
    app.config['SPOTIFY_REDIRECT_URI'] = os.getenv("REDIRECT_URI")

    # Other configuration options could be added here

    # Import and register blueprints
    from . import routes  # Import the routes module
    app.register_blueprint(routes.bp)

    return app
