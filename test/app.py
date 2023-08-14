import os
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

client_id = os.getenv("bbdc1b66814b402a934517c6d913f288")
client_secret = os.getenv("0b8a4dbe8d244614b7a4ebbc10b19fec")
redirect_uri = os.getenv("http://localhost:5000/auth/spotify/callback")

authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
scope = ["user-read-current-playing", "user-top-read", "user-read-email"]

@app.route('/')
def index():
    spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = spotify.authorization_url(authorization_base_url)
    session['spotify_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    if request.args.get('state') != session.pop('spotify_state', None):
        return "Error: State mismatch. Possible CSRF attack."

    spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)
    token = spotify.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    session['token'] = token

    return redirect('/profile')

@app.route('/profile')
def profile():
    token = session.get('token')
    if token is None:
        return "Error: No access token found."

    spotify = OAuth2Session(client_id, token=token)
    profile = spotify.get('https://api.spotify.com/v1/me').json()

    top_artists = spotify.get('https://api.spotify.com/v1/me/top/artists').json()

    return render_template('profile.html', profile=profile, top_artists=top_artists)

if __name__ == "__main__":
    # Run the app with SSL support
    app.run(debug=True, ssl_context=('server.crt', 'server.key'))
