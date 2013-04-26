
import json
import os

from httplib2 import Http

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.utils import timezone
import datetime

from oauth2client.client import OAuth2WebServerFlow, TokenRevokeError
from apiclient.discovery import build

from models import GoogleAccount


def _get_flow():
    return OAuth2WebServerFlow(
        client_id=os.getenv("GOOGLE_API_KEY"),
        client_secret=os.getenv("GOOGLE_API_SECRET_KEY"),
        #https://www.googleapis.com/auth/youtube.readonly,
        scope='https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly',
        redirect_uri='http://localtest.channelfactory.com:8000/acct/oauth2callback')
        # request_visible_actions="http://schemas.google.com/AddActivity")


@login_required
def oauth_start(request):
    try:
        acct = GoogleAccount.objects.get(user=request.user)
    except GoogleAccount.DoesNotExist:
        acct = None

    return render_to_response("oauth/start.html", {'hasCreds': (acct and not acct.credentials.invalid)}, RequestContext(request))


@login_required
def oauth_authorize(request):
    oauth_revoke_auth(request)
    flow = _get_flow()
    return redirect(flow.step1_get_authorize_url())

@login_required
def oauth_revoke_auth(request):
    try:
        acct = GoogleAccount.objects.get(user=request.user)
    except GoogleAccount.DoesNotExist:
        pass
    else:
        if not acct.credentials.invalid:
            try:
                acct.credentials.revoke(Http())
            except TokenRevokeError as e:
                print e
            else:
                acct.save()
    return redirect('accounts.views.oauth_start')


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

    print credentials.to_json()

    return redirect('accounts.views.oauth_start')


@login_required
def oauth_test(request):
    try:
        acct = GoogleAccount.objects.get(user=request.user)
    except GoogleAccount.DoesNotExist:
        acct = None

    if not acct or acct.credentials.invalid:
        return redirect('accounts.views.oauth_start')

    http = acct.credentials.authorize(Http())
    ytService = build('youtube', 'v3', http=http)
    ytaService = build('youtubeAnalytics', 'v1', http=http)

    output = ""
    videos = []

    channelResponse = ytService.channels().list(mine=True, part="id,contentDetails").execute()
    if 'items' not in channelResponse or len(channelResponse['items']) == 0:
        raise Http404
    channel = channelResponse['items'][0]
    channelId = channel['id']
    uploadListId = channel['contentDetails']['relatedPlaylists']['uploads']
    videoResponse = ytService.playlistItems().list(playlistId=uploadListId, part="snippet", maxResults=20).execute()
    for video in videoResponse['items']:
        videos.append((video['snippet']['resourceId']['videoId'], video['snippet']['title']))

    analyticsOpts = {'ids':'channel==%s' % channelId,
                     'start_date':'2013-01-01',
                     'end_date':'2013-05-01',
                     "sort": "month",
                     'metrics':"views",
                     'dimensions':"month"}

    # for n in range(0, 3):
    #     if analyticsResponse['columnHeaders'][n]['name'] == "video":
    #         xVid = n
    #     elif analyticsResponse['columnHeaders'][n]['name'] == "month":
    #         xMonth = n
    #     elif analyticsResponse['columnHeaders'][n]['name'] == "views":
    #         xViews = n
    #
    # for data in analyticsResponse['rows']:
    #     videos[data[xVid]]['views'].append( (data[xMonth], data[xViews]) )

    for vid in videos:
        analyticsResponse = ytaService.reports().query(filters="video==%s" % vid[0], **analyticsOpts).execute()

        if 'rows' not in analyticsResponse:
            continue

        output += "Monthly views for \"%s\" http://www.youtube.com/watch?v=%s\n" % (vid[1], vid[0])

        for data in analyticsResponse['rows']:
            output += "    %s - %5d\n" % (data[0], data[1])
        output += "\n"

    acct.save()

    return HttpResponse(output, mimetype="text/plain")


@login_required
def oauth_gplus_moment(request):
    try:
        acct = GoogleAccount.objects.get(user=request.user)
    except GoogleAccount.DoesNotExist:
        acct = None

    if not acct or acct.credentials.invalid:
        return redirect('accounts.views.oauth_start')

    service = build('plus' ,'v1', http=acct.credentials.authorize(Http()))

    output = ""

    moment_to_insert = {
        "type" : "http://schemas.google.com/AddActivity",
        "target" : {

#            "id": "target-id-1",
#            "type":"http://schemas.google.com/AddActivity",
#            "name": "The Google+ Platform",
#            "description": "A page that describes just how awesome Google+ is!",
#            "image": "https://developers.google.com/+/plugins/snippet/examples/thing.png"

            "url" : "http://www.channelfactory.com"
        }
    }


    google_moment_insert = service.moments().insert(collection="vault", userId="me", body=moment_to_insert)
    google_moment_insert.execute()

    output = ""
    moments_list = service.moments().list(collection='vault',userId='me').execute()
    output += str(moments_list)

    return HttpResponse(output, mimetype="text/plain")