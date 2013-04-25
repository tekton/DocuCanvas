
import json
import os

from httplib2 import Http

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q

from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build

from models import GoogleAccount


def _get_flow():
    return OAuth2WebServerFlow(
        client_id=os.getenv("GOOGLE_API_KEY"),
        client_secret=os.getenv("GOOGLE_API_SECRET_KEY"),
        scope='https://www.googleapis.com/auth/youtube.readonly', 
        redirect_uri='http://localtest.channelfactory.com:8000/acct/oauth2callback')


@login_required
def oauth_start(request):
    hasCreds = GoogleAccount.objects.filter(user=request.user).exists()
    return render_to_response("oauth/start.html", {'hasCreds':hasCreds}, RequestContext(request))


@login_required
def oauth_authorize(request):
    flow = _get_flow()
    return redirect(flow.step1_get_authorize_url())


@login_required
def oauth_callback(request):
    if "code" not in request.GET:
        raise Http404
    flow = _get_flow()
    credentials = flow.step2_exchange(request.GET['code'])

    acct, created = GoogleAccount.objects.get_or_create(user=request.user, defaults={'credentials':credentials})
    if not created:
        acct.credentials = credentials
        acct.save()

    return redirect('accounts.views.oauth_start')


@login_required
def oauth_test(request):
    try:
        acct = GoogleAccount.objects.get(user=request.user)
    except GoogleAccount.DoesNotExist:
        return redirect('accounts.views.oauth_start')

    credentials = acct.credentials

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

    acct.credentials = credentials
    acct.save()

    return HttpResponse(output, mimetype="text/plain")
