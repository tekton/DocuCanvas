# Create your views here.
import hashlib
import urllib
import urlparse
import json
import subprocess
import facebook

import oauth2 as oauth

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from facebook.models import FacebookProfile, FBNotification


APP_ID				= "441109929301348"
APP_SECRET			= "8c218d00b2384a38c7938e4b74156da1"
ACCESS_TOKEN_URL	= "https://graph.facebook.com/oauth/access_token"
REQUEST_TOKEN_URL	= "https://www.facebook.com/dialog/oauth"
CHECK_AUTH			= "https://graph.facebook.com/me"
GRAPH_URL			= "https://graph.facebook.com/"


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
		content_dict = json.loads(content)
		userid = content_dict['id']
		try:
			print "are we still here?!?!"
			myprofile = FacebookProfile.objects.get(user=request.user)
			myprofile.update_token(access_token)
		except:
			myprofile = FacebookProfile(user=request.user, facebook_id=userid, image_url=(GRAPH_URL + content_dict['username'] + '/picture'), access_token=access_token)
			myprofile.get_remote_image()
			myprofile.save()
		# user = authenticate(username=profile.user.username, password=hashlib.new(profile.fb_uid).hexdigest())
		# login(request,user)
	return redirect('dashboard.views.home')


def facebookConnect(request):
	callback_url = 'http://' + request.META['HTTP_HOST'] + '/facebook/getAccessToken'
	return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&redirect_uri=%s&scope=%s' % (APP_ID, urllib.quote_plus(callback_url),'email,user_photos'))

'''
def notification(request, user_id):
	callback_url = 'http://' + request.META['HTTP_HOST'] + '/facebook/updateToken/' + user_id
	return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&redirect_uri=%s&scope=%s' % (APP_ID, urllib.quote_plus(callback_url), 'email,user_photos'))


def updateToken(request, user_id):
	code = request.GET.get('code')
	print request.GET
	consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
	client = oauth.Client(consumer)
	redirect_uri = 'http://localhost:8000/facebook/updateToken/' + user_id
	request_url = ACCESS_TOKEN_URL + '?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (APP_ID, redirect_uri, APP_SECRET, code)
	resp, content = client.request(request_url, 'GET')
	access_token = dict(urlparse.parse_qsl(content))['access_token']
	request_url = CHECK_AUTH + '?access_token=%s' % access_token
	if resp['status'] == '200':
		resp, content = client.request(request_url, 'GET')
		content_dict = simplejson.loads(content)
		userid = content_dict['id']
		try:
			myprofile = FacebookProfile.objects.get(user=request.user)
			myprofile.updateToken(access_token)
			myprofile.save()
		except Exception, e:
			print "Couldn't find user facebook profile object"
	return redirect('facebook.views.sendNotification', user_id)
'''

def sendNotification(request, user_id):
	code = request.GET.get('code')
	consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
	client = oauth.Client(consumer)
	redirect_uri = 'http://localhost:8000/facebook/notifications/' + user_id
	request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grand_type=client_credentials' % (APP_ID, APP_SECRET)
	resp, cont = client.request(request_url, 'GET')
	print cont
	access_token = dict(urlparse.parse_qsl(cont))['access_token']
	print 'ACCESS TOKEN:'
	print access_token
	print 'END ACCESS TOKEN'
	try:
		target_user = User.objects.get(pk=user_id)
	except Exception, e:
		print "Could not find user"
	try:
		facebook = FacebookProfile.objects.get(user=target_user)
	except Exception, e:
		print "Could not find facebook profile"
	content = "test"
	request_url = GRAPH_URL + facebook.facebook_id + "/notifications?access_token=%s&template=%s&href=%s" % (access_token, content, 'http://' + request.META['HTTP_HOST'])
	resp, cont = client.request(request_url, 'POST')
	print resp
	notification = FBNotification(sender=request.user, fb_profile=facebook, text=content)
	return redirect('dashboard.views.home')


def getAppAccessToken(request, user_id):
	callback_url = 'http://' + request.META['HTTP_HOST'] + '/facebook/notifications/' + user_id
	return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grand_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))
