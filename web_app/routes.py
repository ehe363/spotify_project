from flask import Blueprint, redirect, session, request
from requests_oauthlib import OAuth2Session
from web_app import create_app

bp = Blueprint("routes", __name__)

# ... other code ...

@bp.route('/auth/spotify/callback')
def spotify_callback():
    app = create_app()
    spotify = OAuth2Session(
        app.config['SPOTIFY_CLIENT_ID'],
        scope=scope,
        redirect_uri=app.config['SPOTIFY_REDIRECT_URI']
    )

    token_url = "https://accounts.spotify.com/api/token"
    token = spotify.fetch_token(
        token_url,
        client_secret=app.config['SPOTIFY_CLIENT_SECRET'],
        authorization_response=request.url
    )

    # Now you can use the 'token' to make requests to the Spotify API

    return "Callback endpoint"
