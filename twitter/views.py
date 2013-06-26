from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from issues.models import Issue, IssueComment
from twitter.models import TwitterProfile
from twitter.forms import TwitterForm

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


def tweeter(request):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	myuser = 'RyanSha61097211'
	api.send_direct_message(screen_name=myuser, text='Hello!')


def add_twitter_acct(request):
	twat = TwitterProfile()
	if request.method == 'POST':
		twatForm = TwitterForm(request.POST, instance=twat)
		if twatForm.is_valid():
			try:
				twat.save()
			except Exception, e:
				print e
			return redirect('dashboard.views.home')
		else:
			print "form not valid"
	twatForm = TwitterForm(instance=twat)
	return render_to_response('twitter/twit_form.html', {'form': twatForm}, context_instance=RequestContext(request))


def send_dm_comment_update(request, user_id, issue_comment_id):
	myuser = User.objects.get(pk=user_id)
	twat = TwitterProfile.objects.get(user=myuser)
	comment = IssueComment.objects.get(pk=issue_comment_id)
	issue = comment.issue
	project = issue.project


def send_dm_new_issue(request, user_id, issue_id):
	myuser = User.objects.get(pk=user_id)
	twat = TwitterProfile.objects.get(user=myuser)
	issue = Issue.objects.get(pk=issue_id)
	project = issue.project

def send_dm_all_new_issue(request, issue_id):
	twat = TwitterProfile.objects.all()
	issue = Issue.objects.get(pk=issue_id)
	project = issue.project
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	content = "New issue in project, " + project.name + "\n" + "Issue Summary: " + issue.summary
	print issue.summary
	for twit in twat:
		api.send_direct_message(screen_name=twit.user_name, text=content)
	return redirect('dashboard.views.home')
