
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
        scope='https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly',
        redirect_uri='http://localtest.channelfactory.com:8000/acct/oauth2callback')
        request_visible_actions="http://schemas.google.com/AddActivity")


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
                     'metrics':"views,likes",
                     'dimensions':"month"}

    for vid in videos:
        analyticsResponse = ytaService.reports().query(filters="video==%s" % vid[0], **analyticsOpts).execute()

        if 'rows' not in analyticsResponse:
            continue

        output += "Monthly stats for \"%s\" http://www.youtube.com/watch?v=%s\n" % (vid[1], vid[0])
        output += "%11s %7s %7s\n" % ('Month', 'Views', 'Likes')
        for data in analyticsResponse['rows']:
            output += "%11s %7d %7d\n" % (data[0], data[1], data[2])
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

@login_required
def yt_videos_list(request):
    try:
        acct = GoogleAccount.objects.get(user=request.user)
    except GoogleAccount.DoesNotExist:
        acct = None

    if not acct or acct.credentials.invalid:
        return redirect('accounts.views.oauth_start')

    service = build('youtube' ,'v3', http=acct.credentials.authorize(Http()))


    output = ""

    channels = service.channels().list(mine=True, part="contentDetails").execute()
    for channel in channels['items']:
        listId = channel['contentDetails']['relatedPlaylists']['uploads']
        output += "Videos in list %s<br/>\n" % listId
        videos = service.playlistItems().list(playlistId=listId, part="snippet", maxResults=20).execute()
        for video in videos['items']:
            output += "\"%s\" - http://www.youtube.com/watch?v=%s<br/>\n" % (video['snippet']['title'], video['snippet']['resourceId']['videoId'])

        output += "\n"

    ########################
    #       activity       #
    ########################

    activityPartsRequested = "id,snippet,contentDetails"
    activityMineFlag = True
    activityPublishedBefore = None
    activityChannelId = None
    activityPageToken = None
    activityMaxResults = 50
    activityHome = None
    activityPublishedAfter = None

    activityRequest = service.activities().list(
        part=activityPartsRequested,
        pageToken=activityPageToken,
        publishedBefore=activityPublishedBefore,
        channelId=activityChannelId,
        mine=activityMineFlag,
        maxResults=activityMaxResults,
        home=activityHome,
        publishedAfter=activityPublishedAfter,
    )

    output += "<div style='border: 1px solid black; margin: 5px;'>Activities<br/>\r\n"

    while activityRequest is not None:
        activities = activityRequest.execute()
        for activity in activities["items"]:
            #output += "%s <br/>\r\n" % (activity["snippet"]["type"] )
            if activity["snippet"]["type"] == "comment":
                output += "Comment: %s<br/>\r\n<br/>\r\n" % activity["snippet"]["description"]
            elif activity["snippet"]["type"] == "subscription":
                output += "Subscription: %s<br/>\r\n<br/>\r\n" % activity["contentDetails"]["subscription"]["resourceId"]["channelId"]
                output += "<textarea>%s</textarea><br/>\r\n" % json.dumps(activity)
            elif activity["snippet"]["type"] == "like":
                output += "Like: %s<br/>\r\n<br/>\r\n" % activity["snippet"]["description"]
            else:
                output += "<textarea>%s</textarea><br/>\r\n<br/>\r\n" % json.dumps(activity)

        activityRequest = service.activities().list_next(previous_request=activityRequest, previous_response=activities)

    #output += "<textarea>%s</textarea><br/>\r\n" % json.dumps(activities)

    output += "</div>"

    ########################
    #       channels       #
    ########################

    channelPartsRequested = "id,snippet,contentDetails,statistics,topicDetails"
    managedByMeFlag = False  # if this is True, the onBehalfOfContentOwnerId must be the ID of the content owner
    onBehalfOfContentOwnerId = None
    pageTokenFlag = None
    idList = None  # None = get all, otherwise needs to be a comma seperated list of youtube channel IDs
    maxResultsInt = 50  # results per page (0-50)
    mineFlag = True  # Return only channels owned by the authenticated user
    mySubscribersFlag = True  # set to true if you want to retrieve a list of subscribed users
    categoryIdFlag = None  # limits the channels requested by category ID

    channelsRequest = service.channels().list(
        part=channelPartsRequested, 
#        managedByMe=managedByMeFlag, 
        #onBehalfOfContentOwner=onBehalfOfContentOwnerId, 
        pageToken=pageTokenFlag, 
        id=idList, 
        maxResults=maxResultsInt, 
        mine=mineFlag,
        #mySubscribers=mySubscribersFlag, 
        categoryId=categoryIdFlag
        )
    
    output += "<div style='border: 1px solid black; margin: 5px;'>Channels:<br/>\r\n"
    channels = channelsRequest.execute()
    output += "<textarea>%s</textarea><br/>\r\n" % json.dumps(channels)

    channelsRequest = service.channels().list_next(previous_request=channelsRequest, previous_response=channels)
    channelCounter = 0
    while channelsRequest != None and channelCounter < 1:
        channels = channelsRequest.execute()
        output += "<textarea>%s</textarea><br/>\r\n" % json.dumps(channels)
        #for channel in channels["items"]:
        #    output += "<textarea>%s</textarea><br/>\r\n" % json.dumps(channel)
        channelsRequest = service.channels().list_next(previous_request=channelsRequest, previous_response=channels)
        channelCounter += 1
    output += "</div>"

    ########################
    #    subscriptions     #
    ########################
    resultsPerPage = 50 #0-50, per API documentation
    subscriptionsParts = "snippet,id,contentDetails"
    minePart="true"
    pageCounter = None

    output += "\n<div style='border: 1px solid black'><p>Your subscriptions:</p>\n"
    
    subscriptionsRequest = service.subscriptions().list(part="snippet,id,contentDetails", mine="true", maxResults=resultsPerPage, pageToken=pageCounter)

    while subscriptionsRequest != None:
        subscriptions = subscriptionsRequest.execute()
        for sub in subscriptions["items"]:
            channelId = sub["snippet"]["channelId"]
            channelDescription = sub["snippet"]["description"]

            output += "<div style='border: 1px solid black; margin: 5px; padding: 5px;'>"
            output += "Channel: <a href='http://www.youtube.com/feed/%s/u' target='_blank'>%s</a><br/>\r\n" % (sub["snippet"]["resourceId"]["channelId"], sub["snippet"]["title"])
            output += "Id: %s<br/>\r\n" % channelId
            output += "Description: <pre style='border: 1px solid lightgrey;'>%s</pre><br/>\r\n" % channelDescription
            #output += "<textarea>%s</textarea><br/>\r\n" % json.dumps(sub)
            output += "</div>"
        subscriptionsRequest = service.subscriptions().list_next(previous_request=subscriptionsRequest, previous_response=subscriptions)
    output += "</div>\r\n"    
########################
########################
    acct.save()
    return HttpResponse(output, mimetype="text/html")
