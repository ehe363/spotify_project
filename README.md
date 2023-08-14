# spotify_project

#Setup - Obtain a Spotify Developer API Client ID, Client Secret, specify a redirect URI and place into .env file. Also obtain a ticketmaster API key and place into .env file.

#To authenticate user data: Run the app and authenticate the user data access. Once done, copy entire URL (INCLUDING HTTPS) and paste into the app where prompted.

#Rest of app will then run and match upcoming events with top artists based on the Spotify user's listening history.

#Create a virtual environment:
conda create -n spotify-env python=3.10

#Activate your virtual environment:
conda activate spotify-env

#Install packages:
pip install -r requirements.txt

pip install flask

python app.py

#Run the app:
python -m app
