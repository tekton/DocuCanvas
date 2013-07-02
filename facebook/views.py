# Create your views here.
import hashlib
import urllib
import urlparse
import json
import simplejson
import subprocess
import facebook

import oauth2 as oauth

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from facebook.models import FacebookProfile


APP_ID				= "441109929301348"
APP_SECRET			= "8c218d00b2384a38c7938e4b74156da1"
ACCESS_TOKEN_URL	= "https://graph.facebook.com/oauth/access_token"
REQUEST_TOKEN_URL	= "https://www.facebook.com/dialog/oauth"
CHECK_AUTH			= "https://graph.facebook.com/me"
PHOTO_BASE_URL		= "https://graph.facebook.com/"


def getAccessToken(request):
	code = request.GET.get('code')
	consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
	client = oauth.Client(consumer)
	redirect_uri = 'http://localhost:8000/facebook/getAccessToken'
	request_url = ACCESS_TOKEN_URL + '?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (APP_ID, redirect_uri, APP_SECRET, code)
	resp, content = client.request(request_url, 'GET')
	access_token = dict(urlparse.parse_qsl(content))['access_token']
	request_url = CHECK_AUTH + '?access_token=%s' % access_token
	if resp['status'] == '200':
		resp, content = client.request(request_url, 'GET')
		content_dict = simplejson.loads(content)
		userid = content_dict['id']
		try:
			print "are we still here?!?!"
			myprofile = FacebookProfile.objects.get(user=request.user)
		except:
			myprofile = FacebookProfile(user=request.user, facebook_id=userid, image_url=(PHOTO_BASE_URL + content_dict['username'] + '/picture'))
			myprofile.get_remote_image()
			myprofile.save()
		# user = authenticate(username=profile.user.username, password=hashlib.new(profile.fb_uid).hexdigest())
		# login(request,user)
	return redirect('dashboard.views.home')


def facebookConnect(request):
	callback_url = 'http://' + request.META['HTTP_HOST'] + '/facebook/getAccessToken'
	return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&redirect_uri=%s&scope=%s' % (APP_ID, urllib.quote_plus(callback_url),'email,user_photos'))

