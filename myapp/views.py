from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import google.oauth2.credentials
import google_auth_oauthlib.flow








def hello_world(request):
    return HttpResponse("Helcclo, World!")
def a(request):
        
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret_55352107311-blbqos8se6c3vs86gkdtj0l77mkf0q2d.apps.googleusercontent.com.json',
        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://127.0.0.1:8000/myapp/receptor'

    # Generate URL for request to Google's OAuth 2.0 server.
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    return HttpResponse("alaa re alaa")
def receptor(request):
    return HttpResponse("aleeeele")