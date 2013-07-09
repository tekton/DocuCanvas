from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from projects.models import Project
from issues.models import Issue, IssueComment
from twitter.models import TwitterProfile, Tweet, DMAll, DMIndividual
from twitter.forms import TwitterForm, TweetForm, DMAForm, DMIForm
from notifications.models import Notification, NotificationRecipient

import sys
import tweepy

TWITTER_TWITTER_CONSUMER_KEY		= '8nY1q44v3YWGgqfP2eCjFg'
TWITTER_CONSUMER_SECRET		= 's2MFyXSLbHTmGbz9qBGNFubaeTRivsLJpHsnESnlfE'
TWITTER_TWITTER_ACCESS_KEY			= '1535252624-YWB7X7lbBwdmzKmWA5Aiep7wis3ARc0EA8hDqIj'
TWITTER_TWITTER_ACCESS_SECRET		= 'MBrOvB34fuQtQ8vzyfMcA48ZbEhg3zpqgMvAuTSDDk'
# request_token_url	= 'http://twitter.com/oauth/request_token'
# access_token_url	= 'http://twitter.com/oauth/access_token'
# authenticate_url	= 'http://twitter.com/oauth/authenticate'


@login_required
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
	return render_to_response('twitter/twit_form.html', {'form': twatForm}, context_instance=RequestContext(request))


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
def send_dm_comment_update(request, user_id, issue_comment_id):
	if request.user.is_staff:
		myuser = User.objects.get(pk=user_id)
		twat = TwitterProfile.objects.get(user=myuser)
		comment = IssueComment.objects.get(pk=issue_comment_id)
		issue = comment.issue
		project = issue.project
		auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
		api = tweepy.API(auth)
		content = comment.user + " commented on issue " + issue.summary + " in project " + project.name
		if twat.active:
			try:
				api.send_direct_message(screen_name=twat.user_name, text=content)
			except Exception, e:
				print e
	return redirect('dashboard.views.home')


@login_required
def send_dm_new_issue(request, user_id, issue_id):
	if request.user.is_staff:
		myuser = User.objects.get(pk=user_id)
		twat = TwitterProfile.objects.get(user=myuser)
		issue = Issue.objects.get(pk=issue_id)
		project = issue.project
		auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New issue in project, " + project.name + "\n" + "Issue Summary: " + issue.summary
		if twat.active:
			try:
				api.send_direct_message(screen_name=twat.user_name, text=content)
			except Exception, e:
				print e
	return redirect('dashboard.views.home')


@login_required
def send_dm_new_issue_all(request, issue_id):
	if request.user.is_staff:
		twat = TwitterProfile.objects.all()
		issue = Issue.objects.get(pk=issue_id)
		project = issue.project
		auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New issue in project, " + project.name + "\n" + "Issue Summary: " + issue.summary
		print issue.summary
		for twit in twat:
			if twit.active:
				try:
					api.send_direct_message(screen_name=twit.user_name, text=content)
				except Exception, e:
					print "failed to send message to " + twit.user_name
	return redirect('dashboard.views.home')


@login_required
def send_dm_new_project(request, user_id, project_id):
	if request.user.is_staff:
		myuser = User.objects.get(pk=user_id)
		twat = TwitterProfile.objects.get(user=myuser)
		project = Project.objects.get(pk=project_id)
		auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New Project Created! " + project.name
		if twat.active:
			api.send_direct_message(screen_name=twat.user_name, text=content)
	return redirect('dashboard.views.home')


@login_required
def send_dm_new_project_all(request, project_id):
	if request.user.is_staff:
		twat = TwitterProfile.objects.all()
		project = Project.objects.get(pk=project_id)
		auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New Project Created! " + project.name
		for twit in twat:
			if twit.active:
				try:
					api.send_direct_message(screen_name=twit.user_name, text=content)
				except Exception, e:
					print "faield to send message to " + twit.user_name
	return redirect('dashboard.views.home')


@login_required
def new_project_tweet(request, project_id):
	if request.user.is_staff:
		project = Project.objects.get(pk=project_id)
		auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
		api = tweepy.API(auth)
		content = "New Project Created! " + project.name
		api.update_status(status=content)
	return redirect('dashboard.views.home')


def new_tweet(request):
	if request.user.is_staff:
		if request.method == 'POST':
			content = request.POST['twit-content']
			tweet = Tweet(tweet_user=request.user, content=content)
			if content != '':
				auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
				auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
				api = tweepy.API(auth)
				try:
					api.update_status(status=tweet.content)
					tweet.save()
				except Exception, e:
					print e
				return redirect('dashboard.views.home')
	return render_to_response('twitter/new_tweet.html', {}, context_instance=RequestContext(request))
