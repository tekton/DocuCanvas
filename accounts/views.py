
import json

from httplib2 import Http

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q

from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build

import os


def _get_google_keys():
    returnVal = {}
    returnVal["devKey"] = os.getenv("GOOGLE_API_KEY","")
    returnVal["devSecretKey"] = os.getenv("GOOGLE_API_SECRET_KEY","")
    return returnVal


def _get_flow():
    gSettings = _get_google_keys()
    return OAuth2WebServerFlow(
        client_id=gSettings['devKey'], 
        client_secret=gSettings['devSecretKey'], 
        scope='https://www.googleapis.com/auth/youtube.readonly', 
        redirect_uri='http://localtest.channelfactory.com:8000/acct/oauth2callback')


def oauth_test(request):
    flow = _get_flow()
    return redirect(flow.step1_get_authorize_url())


def oauth_callback(request):
    if "code" not in request.GET:
        raise Http404
    flow = _get_flow()
    credentials = flow.step2_exchange(request.GET['code'])
    
    service = build('youtube', 'v3', http=credentials.authorize(Http()))

    output = ""

    channels = service.channels().list(mine=True, part="contentDetails").execute()
    for channel in channels['items']:
        listId = channel['contentDetails']['relatedPlaylists']['uploads']
        output += "Videos in list %s\n" % listId
        videos = service.playlistItems().list(playlistId=listId, part="snippet", maxResults=20).execute()
        for video in videos['items']:
            output += "\"%s\" - http://www.youtube.com/watch?v=%s\n" % (video['snippet']['title'], video['snippet']['resourceId']['videoId'])

        output += "\n"

    return HttpResponse(output, mimetype="text/plain")
