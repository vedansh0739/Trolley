from flask import Flask, redirect, session, url_for, request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask_cors import CORS
import logging
logging.basicConfig(level=logging.DEBUG)
from flask import Flask, request, jsonify, render_template


from flask import jsonify
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'mkv', 'wmv'}
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key='some_key'
import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask import Flask, request, jsonify
import os

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'mkv', 'wmv'}

import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
import googleapiclient.discovery

from googleapiclient.http import MediaFileUpload


@app.route("/authparam")
def authparam():
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret_39212534978-m8o47udmc5sfp08ud3u0lt2arp2lrps2.apps.googleusercontent.com.json',
        scopes=['https://www.googleapis.com/auth/youtube.upload',])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://127.0.0.1:5000/receive'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    session['state'] = state
    app.logger.debug(f"Generated authorization URL: {authorization_url}")
    app.logger.debug(f"Authparam route session data: {session}")
    return redirect(authorization_url)



@app.route("/receive")
def receive():
    
    state = session['state']
    app.logger.debug(f"Receive route initial session data: {session}")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret_39212534978-m8o47udmc5sfp08ud3u0lt2arp2lrps2.apps.googleusercontent.com.json',
        scopes=['https://www.googleapis.com/auth/youtube.upload'],
        state=state)
    flow.redirect_uri = url_for('receive', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}
    app.logger.debug(f"Authorization response URL: {authorization_response}")
    app.logger.debug(f"Receive route updated session data: {session}")
    return "<p>Hreceived!</p>"

@app.route("/get_credentials")
def get_credentials():
    app.logger.debug(f"Get credentials route session data: {session}")
    creds_data = session.get('credentials')
    app.logger.debug(type(creds_data))
    if not creds_data:
        
        return jsonify(error="No credentials available"), 400
        

    return jsonify(creds_data)
@app.route('/play_video')
def play_video():
    return render_template("video_player.html")

@app.route('/approve_video')
def approve_video():
    return "video is being uploaded"

@app.route("/buildapi",methods=['GET'])
def buildapi():
    creds_data = session.get('credentials')
    if not creds_data:
        return "No credentials available", 400
    credentials = Credentials(token=creds_data['token'],
                            refresh_token=creds_data['refresh_token'],
                            token_uri=creds_data['token_uri'],
                            client_id=creds_data['client_id'],
                            client_secret=creds_data['client_secret'],
                            scopes=creds_data['scopes'])
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCjQh9iAczX9tT3r-xVIGMMdwfjuDGJ-8E"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
        )
    request = youtube.videos().insert(
        part="snippet,status",
        body={
        "snippet": {
            "categoryId": "22",
            "description": "Description of uploaded video.",
            "title": "Test video upload."
        },
        "status": {
            "privacyStatus": "private"
        }
        },
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload("video.MOV")
    )
    response = request.execute()
    print(response)   
    
    

    return "<p>Hello, World!</p>"
@app.route('/upload_video', methods=['POST'])
def upload_video():
    video_file = request.files.get('video')
    
    if not video_file:
        return jsonify({"error": "No video file found!"}), 400

    # Save the video in the static directory
    video_path = f"./static/{video_file.filename}"
    video_file.save(video_path)

    # Return the URL to play the video
    video_url = f"/static/{video_file.filename}"
    return render_template("video_player.html", video_url=video_url)




if __name__ == '__main__':
    app.run(debug=True)
    