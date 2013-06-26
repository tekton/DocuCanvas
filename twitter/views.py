from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from twitter.models import TwitterProfile

import sys
import tweepy

CONSUMER_KEY		= '8nY1q44v3YWGgqfP2eCjFg'
CONSUMER_SECRET		= 's2MFyXSLbHTmGbz9qBGNFubaeTRivsLJpHsnESnlfE'
ACCESS_KEY			= '1535252624-YWB7X7lbBwdmzKmWA5Aiep7wis3ARc0EA8hDqIj'
ACCESS_SECRET		= 'MBrOvB34fuQtQ8vzyfMcA48ZbEhg3zpqgMvAuTSDDk'
# consumer			= oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
# client				= oauth.Client(consumer)
request_token_url	= 'http://twitter.com/oauth/request_token'
access_token_url	= 'http://twitter.com/oauth/access_token'
authenticate_url	= 'http://twitter.com/oauth/authenticate'


'''
def twitter_login(request):
	resp, content = client.request(request_token_url, 'GET')
	if resp['status'] != '200':
		raise Exception("Invalid response from Twitter.")
	request.session['request_token'] = dict(cgi.parse_qsl(content))
	url = '%s?oauth_token=%s' % (authenticate_url, request.session['request_token']['oauth_token'])
	return HttpResponseRedirect(url)
'''

def tweeter(request):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	myuser = 'RyanSha61097211'
	api.send_direct_message(screen_name=myuser, text='Hello!')