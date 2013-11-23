
import json
import os

from httplib2 import Http

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.utils import timezone
import datetime

import celery
import redis

from oauth2client.client import OAuth2WebServerFlow, TokenRevokeError
from apiclient.discovery import build

from models import GoogleAccount, Account, UserTemplates

from forms import UserTemplatesForm


def _get_flow():
    return OAuth2WebServerFlow(
        client_id=os.getenv("GOOGLE_API_KEY"),
        client_secret=os.getenv("GOOGLE_API_SECRET_KEY"),
        scope='https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly',
        redirect_uri='http://localtest.channelfactory.com:8000/acct/oauth2callback',
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


# @login_required
# def oauth_test(request):
#     try:
#         acct = GoogleAccount.objects.get(user=request.user)
#     except GoogleAccount.DoesNotExist:
#         acct = None
#
#     if not acct or acct.credentials.invalid:
#         return redirect('accounts.views.oauth_start')
#
#     acct.save()
#
#     return HttpResponse(output, mimetype="text/plain")


@celery.task
def setAssignable(account_q):
    try:
        account = Account.objects.get(pk=account_q)
    except Exception as e:
        print "Unable to get account"
        print e
    account.assignable = True
    try:
        account.save()
    except Exception as e:
        print "Unable to save account update"
        print e


@login_required
def assignTemplateForView(request):
    """
        accept post, else use get function
    """
    if request.method == "POST":
        form = UserTemplatesForm(request.POST)  #, instance=temp)
        try:
            form.full_clean()
            itm = form.save()
            redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')  # this is for the heroku install!
            r = redis.from_url(redis_url)
            print dir(itm)
            try:
                x = r.hset(itm.user.id, itm.viewName, itm.pathToTemplate)
                print x
            except Exception as e:
                print e
        except Exception as e:
            print e
            print form.errors
    else:
        form = UserTemplatesForm(initial={"user": request.user})
    return render_to_response("user/user_template_form.html", {'form': form}, RequestContext(request))



def cache_checkUserTemplate(user, view_name):
    '''
        Ask Redis for a view from the account view hash
    '''
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')  # this is for the heroku install!
    r = redis.from_url(redis_url)
    template_in_redis = r.hget(user, view_name)
    if template_in_redis:
        print template_in_redis
        return template_in_redis
    else:
        return False


@celery.task
def cache_populateUserTemplates():
    """
        cycle through possible view_names and Accounts, if something is set populate the cache
    """
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')  # this is for the heroku install!
    r = redis.from_url(redis_url)
    templates = UserTemplates.objects.all()
    for template in templates:
        try:
            r.hset(template.user, template.viewName, template.pathToTemplate)
        except Exception as e:
            print "Unable to set template in cache: {}".format(str(e))
    return True

