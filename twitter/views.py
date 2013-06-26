from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from projects.models import Project
from issues.models import Issue, IssueComment
from twitter.models import TwitterProfile
from twitter.forms import TwitterForm

import sys
import tweepy

CONSUMER_KEY		= '8nY1q44v3YWGgqfP2eCjFg'
CONSUMER_SECRET		= 's2MFyXSLbHTmGbz9qBGNFubaeTRivsLJpHsnESnlfE'
ACCESS_KEY			= '1535252624-YWB7X7lbBwdmzKmWA5Aiep7wis3ARc0EA8hDqIj'
ACCESS_SECRET		= 'MBrOvB34fuQtQ8vzyfMcA48ZbEhg3zpqgMvAuTSDDk'
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
				twits = TwitterProfile.objects.all()
			except Exception, e:
				print e
			# Check to make sure username does not already exist in database
			for twit in twits:
				if twit.user_name == twat.user_name:
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
	return render_to_response('twitter/twit_form.html', {'form': twatForm}, context_instance=RequestContext(request))


def remove_twitter_acct(request):
	myuser = request.user
	twat = TwitterProfile(user=user)
	twat.delete()
	print "Account Deleted"
	return redirect('dashboard.views.home')


def send_dm_comment_update(request, user_id, issue_comment_id):
	if request.user.is_staff:
		myuser = User.objects.get(pk=user_id)
		twat = TwitterProfile.objects.get(user=myuser)
		comment = IssueComment.objects.get(pk=issue_comment_id)
		issue = comment.issue
		project = issue.project
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		content = comment.user + " commented on issue " + issue.summary + " in project " + project.name
	return redirect('dashboard.views.home')


def send_dm_new_issue(request, user_id, issue_id):
	if request.user.is_staff:
		myuser = User.objects.get(pk=user_id)
		twat = TwitterProfile.objects.get(user=myuser)
		issue = Issue.objects.get(pk=issue_id)
		project = issue.project
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New issue in project, " + project.name + "\n" + "Issue Summary: " + issue.summary
	return redirect('dashboard.views.home')


def send_dm_new_issue_all(request, issue_id):
	if request.user.is_staff:
		twat = TwitterProfile.objects.all()
		issue = Issue.objects.get(pk=issue_id)
		project = issue.project
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New issue in project, " + project.name + "\n" + "Issue Summary: " + issue.summary
		print issue.summary
		for twit in twat:
			try:
				api.send_direct_message(screen_name=twit.user_name, text=content)
			except Exception, e:
				print "failed to send message to " + twit.user_name
	return redirect('dashboard.views.home')


def send_dm_new_project(request, user_id, project_id):
	if request.user.is_staff:
		twat = TwitterProfile.objects.get(pk=user_id)
		project = Project.objects.get(pk=project_id)
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New Project Created! " + project.name
		api.send_direct_message(screen_name=twat.user_name, text=content)
	return redirect('dashboard.views.home')


def send_dm_new_project_all(request, project_id):
	if request.user.is_staff:
		twat = TwitterProfile.objects.all()
		project = Project.objects.get(pk=project_id)
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New Project Created! " + project.name
		for twit in twat:
			try:
				api.send_direct_message(screen_name=twit.user_name, text=content)
			except Exception, e:
				print "faield to send message to " + twit.user_name
	return redirect('dashboard.views.home')


def new_project_tweet(request, project_id):
	if request.user.is_staff:
		project = Project.objects.get(pk=project_id)
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New Project Created! " + project.name
		api.update_status(status=content)
	return redirect('dashboard.views.home')



