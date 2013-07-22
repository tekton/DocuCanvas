import hashlib
import urllib
import urlparse
import json
import subprocess
import facebook
import tweepy

import oauth2 as oauth

from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth.decorators import login_required
from socialplatform.models import FacebookProfile, FBNotification, TwitterProfile, Tweet, DMAll, DMIndividual
from socialplatform.forms import TwitterForm, TweetForm, DMAForm, DMIForm, FacebookPermissions
from notifications.models import Notification, NotificationRecipient
from helpdesknew.models import HelpRequest
from projects.models import Project
from polls.models import Poll

# Facebook API info
APP_ID                  = "441109929301348"
APP_SECRET              = "8c218d00b2384a38c7938e4b74156da1"

# Facebook API urls
ACCESS_TOKEN_URL        = "https://graph.facebook.com/oauth/access_token"
REQUEST_TOKEN_URL       = "https://www.facebook.com/dialog/oauth"
CHECK_AUTH              = "https://graph.facebook.com/me"
GRAPH_URL               = "https://graph.facebook.com/"
    
# Twitter API info
TWITTER_CONSUMER_KEY    = '8nY1q44v3YWGgqfP2eCjFg'
TWITTER_CONSUMER_SECRET = 's2MFyXSLbHTmGbz9qBGNFubaeTRivsLJpHsnESnlfE'
TWITTER_ACCESS_KEY      = '1535252624-YWB7X7lbBwdmzKmWA5Aiep7wis3ARc0EA8hDqIj'
TWITTER_ACCESS_SECRET   = 'MBrOvB34fuQtQ8vzyfMcA48ZbEhg3zpqgMvAuTSDDk'


@login_required
def getAccessToken(request):
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/getAccessToken'
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (APP_ID, redirect_uri, APP_SECRET, code)
    resp, content = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(content))['access_token']
    request_url = CHECK_AUTH + '?access_token=%s' % access_token
    if resp['status'] == '200':
        resp, content = client.request(request_url, 'GET')
        content_dict = json.loads(content)
        userid = content_dict['id']
        try:
            myprofile = FacebookProfile.objects.get(user=request.user)
            myprofile.active = True
            myprofile.update_token(access_token)
        except:
            myprofile = FacebookProfile(user=request.user, facebook_id=userid, image_url=(GRAPH_URL + content_dict['username'] + '/picture'), access_token=access_token)
            myprofile.get_remote_image()
            myprofile.active = True
            myprofile.save()
        # user = authenticate(username=profile.user.username, password=hashlib.new(profile.fb_uid).hexdigest())
        # login(request,user)
    return redirect('dashboard.views.home')


@login_required
def facebookConnect(request):
    try:
        facebook = FacebookProfile.objects.get(user=request.user)
        facebook.active = True
        facebook.save()
        return redirect('dashboard.views.home')
    except Exception, e:
        print e
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/getAccessToken'
    return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&redirect_uri=%s&scope=%s' % (APP_ID, urllib.quote_plus(callback_url),'email,user_photos'))


@login_required
def sendTestNotification(request, user_id):
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/notifications_test/' + user_id
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        target_user = User.objects.get(pk=user_id)
    except Exception, e:
        print "Could not find user"
    try:
        facebook = FacebookProfile.objects.get(user=target_user)
    except Exception, e:
        print "Could not find facebook profile"
    content = "you+seem+like+a+bitch"
    request_url = GRAPH_URL + facebook.facebook_id + "/notifications?access_token=%s&template=%s&href=%s" % (access_token, content, 'http://gadget.channelfactory.com:81')
    resp, cont = client.request(request_url, 'POST')
    print resp
    notification = FBNotification(sender=request.user, fb_profile=facebook, text=content)
    return redirect('dashboard.views.home')


@login_required
def getAppAccessToken(request, user_id):
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/notifications_test/' + user_id
    return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grand_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))


@login_required
def add_twitter_acct(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    twat = TwitterProfile()
    if request.method == 'POST':
        twatForm = TwitterForm(request.POST, instance=twat)
        if twatForm.is_valid():
            try:
                twits = TwitterProfile.objects.all()
            except Exception, e:
                print e
            # Check to make sure username does not already exist in database
            for twit in twits:
                if twit.user_name == twat.user_name:
                    if not twit.active:
                        twit.Activate()
                        return redirect('dashboard.views.home')
                    print "user_name already in database"
                    return redirect('dashboard.views.home')
            try:
                twat.save()
            except Exception, e:
                print e
            return redirect('dashboard.views.home')
        else:
            print "form not valid"
    twatForm = TwitterForm(instance=twat)
    return render_to_response('socialplatform/twit_form.html', {'form': twatForm, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def remove_twitter_acct(request):
    if request.method == 'POST':
        myuser = request.user
        twat = TwitterProfile(user=myuser)
        twat.Deactivate()
        print "Account Deactivated"
        return redirect('dashboard.views.home')
    return render_to_response('twitter/deactivate.html', {}, context_instance=RequestContext(request))


@login_required
def access_for_broadcast(request, notification_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
    except Exception, e:
        print e
    if notification.facebook:
        callback_url = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/broadcast/' + notification_id
        return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grand_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))
    return redirect('dashboard.views.home')


@login_required
def social_broadcast(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    message = ""
    for char in notification.message:
        if(char == " "):
            message += "+"
        else:
            message += char
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/broadcast/' + notification_id
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        targets = NotificationRecipient.objects.filter(notification=notification)
    except Exception, e:
        print "No target"

    if notification.facebook:
        for target in targets:
            myuser = target.user
            try:
                facebook = FacebookProfile.objects.get(user=myuser)
                request_url = (GRAPH_URL
                         + facebook.facebook_id 
                         + ("/notifications?access_token=%s&template=%s&href=%s" % (access_token, message, 'http://' + request.META['HTTP_HOST'])))
                if facebook.notifications and facebook.active:
                    resp, cont = client.request(request_url, 'POST')

            except Exception, e:
                print e
    if notification.twitter:
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        for target in targets:
            user = target.user
            try:
                twitter = TwitterProfile.objects.get(user=user)
            except Exception, e:
                print e
            if twitter.active:
                try:
                    api.send_direct_message(screen_name=twitter.user_name, text=notification.message)
                except Exception, e:
                    print e
    return redirect('dashboard.views.home')


@login_required
def broadcast_help(request, help_id):
    message = ""
    try:
        help = HelpRequest.objects.get(pk=help_id)
        user = help.user
    except Exception, e:
        print e
    for char in help.name:
        if(char == " "):
            message += "+"
        else:
            message += char
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/helpbroadcast/' + help_id
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        targets = User.objects.filter(is_staff=True)
        for target in targets:
            print target
    except Exception, e:
        print e
    for target in targets:
        try:
            facebook = FacebookProfile.objects.get(user=target)
            request_url = (GRAPH_URL
                         + facebook.facebook_id 
                         + ("/notifications?access_token=%s&template=%s&href=%s" % (access_token, message, 'http://' + request.META['HTTP_HOST'])))
            if facebook.helpdesk and facebook.active:
                resp, cont = client.request(request_url, 'POST')
        except Exception, e:
            print e
    return redirect('helpdesknew.views.get_help', help_id)


@login_required
def sending_help(request, help_id):
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/helpbroadcast/' + help_id
    return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grand_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))


@login_required
def notify_assignment(request, issue_id):
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/assignbroadcast/' + issue_id
    return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grand_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))


@login_required
def assignment_broadcast(request, issue_id):
    try:
        issue = Issue.objects.get(pk=issue_id)
        user = issue.assigned_to
    except Exception, e:
        print e
    message = "You+have+been+assigned+to+an+issue,+"
    for char in issue.summary:
        if char == " ":
            message += "+"
        else:
            message += char
    message += "+in+"
    for char in issue.project.name:
        if char == " ":
            message += "+"
        else:
            message += char
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/assignbroadcast/' + issue_id
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        facebook = FacebookProfile.objects.get(user=user)
        request_url = (GRAPH_URL
                     + facebook.facebook_id 
                     + ("/notifications?access_token=%s&template=%s&href=%s" % (access_token, message, 'http://' + request.META['HTTP_HOST'])))
        if facebook.issue and facebook.active:
            resp, cont = client.request(request_url, 'POST')
    except Exception, e:
        print e
    return redirect('issues.views.issue_overview', issue_id)


@login_required
def notify_new_poll(request, poll_id):
    try:
        facebook = FacebookProfile.objects.get(user=request.user)
        callback_url = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/newpollbroadcast/' + poll_id
        return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grand_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))
    except Exception, e:
        return redirect('polls.views.poll_overview', poll_id)
    


@login_required
def new_poll_broadcast(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
        targets = FacebookProfile.objects.all()
    except Exception, e:
        print e
    message = 'New+poll+created,+"'
    for char in poll.name:
        if char == " ":
            message += "+"
        else:
            message += char
    message += '"'
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/socialplatform/newpollbroadcast/' + poll_id
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    for target in targets:
        try:
            request_url = (GRAPH_URL
                         + target.facebook_id 
                         + ("/notifications?access_token=%s&template=%s&href=%s" % (access_token, message, 'http://' + request.META['HTTP_HOST'])))
            if target.polls and target.active:
                resp, cont = client.request(request_url, 'POST')
        except Exception, e:
            print e
    return redirect('polls.views.poll_overview', poll_id)


@login_required
def modify_permissions(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        raise e
    try:
        facebook = FacebookProfile.objects.get(user=request.user)
    except Exception, e:
        return redirect('dashboard.views.home')
    if request.method == 'POST':
        permission_form = FacebookPermissions(request.POST, instance=facebook)
        if permission_form.is_valid():
            try:
                facebook = permission_form.save()
            except Exception, e:
                print e
            if not facebook.active:
                facebook.deactivate()
            return redirect('dashboard.views.home')
    else:
        permission_form = FacebookPermissions(instance=facebook)
    return render_to_response('socialplatform/facebook_permissions.html', {'facebook': facebook, 'form': permission_form, 'projects': projects}, context_instance=RequestContext(request))
