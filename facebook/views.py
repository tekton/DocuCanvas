# Create your views here.
import hashlib
import urllib
import urlparse
import json

import oauth2 as oauth

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
# from facebook.models import Facebook


APP_ID				= "441109929301348"
APP_SECRET			= "8c218d00b2384a38c7938e4b74156da1"
ACCESS_TOKEN_URL	= "https://graph.facebook.com/oauth/access_token"
REQUEST_TOKEN_URL	= "https://www.facebook.com/dialog/oauth"
CHECK_AUTH			= "https://graph.facebook.com/me"

'''
def getAccessToken(request):
	consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
	client = oauth.Client(consumer)
	request_url = 'https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grand_type=client_credentials' % (APP_ID, APP_SECRET)
	resp, content = client.request(request_url, 'GET')
	print content
	access_token = dict(urlparse.parse_qsl(content))['access_token']
	if resp['status'] == '200':
		print access_token
	print "hello"
	return redirect('dashboard.views.home')
'''


def getAccessToken(request):
	code = request.GET.get('code')
	consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
	client = oauth.Client(consumer)
	redirect_uri = 'http://' + (request.META['HTTP_HOST']) +'/'
	print redirect_uri
	request_url = ACCESS_TOKEN_URL + '?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (APP_ID, redirect_uri, APP_SECRET, code)
	resp, content = client.request(request_url, 'GET')
	print content
	access_token = dict(urlparse.parse_qsl(content))['access_token']
	request_url = CHECK_AUTH + '?access_token=%s' % access_token
	print access_token
	'''
	if resp['status'] == '200':
		resp, content = client.request(request_url, 'GET')
		content_dict = simplejson.loads(content)
		userid = content_dict['id']
		try:
			profile = Profile.objects.get(fb_uid=userid)
		except:
			profile = register_user(content_dict['first_name'], content_dict['last_name'], content_dict['email']), None, content_dict['username'], 'facebook', userid)
		user = authenticate(username=profile.user.username, password=hashlib.new(profile.fb_uid).hexdigest())
		login(request,user)
		'''
	return HttpResponseRedirect('/')


def facebookConnect(request):
	callback_url = 'http://' + request.META['HTTP_HOST'] + '/'
	return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&redirect_uri=%s&scope=%s' % (APP_ID, urllib.quote_plus(callback_url),'email'))