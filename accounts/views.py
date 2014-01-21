
import json
import os

from httplib2 import Http

from django.contrib.auth.forms import PasswordChangeForm
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

from models import GoogleAccount, Account, UserTemplates, AccountSetting

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
        try:
            print request.POST["viewName"]
            temp = UserTemplates.objects.get(user=request.user, viewName=request.POST["viewName"])
        except:
            temp = UserTemplates()
        form = UserTemplatesForm(request.POST, instance=temp)
        # print dir(form)
        try:
            form.full_clean()
            itm = form.save()
            redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')  # this is for the heroku install!
            r = redis.from_url(redis_url)
            try:
                print "{0} - {1} - {2}".format("user.settings.{}.hash".format(itm.user.id), itm.viewName, itm.pathToTemplate)
                x = r.hset("user.settings.{}.hash".format(itm.user.id), itm.viewName, itm.pathToTemplate)
                print x
            except Exception as e:
                print "post set..."
                print e
                print "...post e"
        except Exception as e:
            print "Clean or save failed..."
            print e
            print form.errors
    else:
        form = UserTemplatesForm(initial={"user": request.user})
    return render_to_response("user/user_template_form.html", {'form': form}, RequestContext(request))



def cache_checkUserTemplate(user, view_name):
    '''
        Ask Redis for a view from the account settings hash
    '''
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')  # this way REDISTOGO_URL can be overridden on an install basis
    r = redis.from_url(redis_url)
    template_in_redis = r.hget("user.settings.{}.hash".format(user.id), view_name)
    if template_in_redis:
        print template_in_redis
        return template_in_redis
    else:
        return False


@celery.task
def cache_populateUserTemplates(single=None):
    """
        cycle through possible view_names and Accounts, if something is set populate the cache
    """
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)
    if single:
        try:
            templates = UserTemplates.objects.get(pk=single)
        except Exception as e:
            print str(e)
            return False
    else:
        templates = UserTemplates.objects.all()
    for template in templates:
        try:
            r.hset("user.settings.{}.hash".format(template.user.id), template.viewName, template.pathToTemplate)
        except Exception as e:
            print "Unable to set template in cache: {}".format(str(e))
    return True


def settings_update(request, setting_to_set, new_value=None):
    if request.method == "POST":
        new_value = request.POST["new_value"]
    # only except post? they have to be logged in anyway though...
    try:  # this could get a get_or_create but that limits us and would just make us write code if we wanted slightly different functionality
        setting = AccountSetting.objects.get(user=request.user, setting_name=setting_to_set)
        if setting.setting_value == new_value:
            return HttpResponse(json.dumps({"msg": "no change"}), content_type='application/json', status=200)
    except Exception as e:
        print "Hoping it just didn't exit yes, just in case :: {}".format(e)
        setting = AccountSetting()
        setting.user = request.user
        setting.setting_name = setting_to_set
    print setting_to_set, new_value
    if setting.setting_value == new_value:
        pass
    else:
        setting.setting_value = new_value
        setting.save()
        # now that it's saved in the DB lets save it in the cache! someday...
        try:
            r = redis.from_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
            r.hset("user.settings.{}.hash".format(request.user.id), setting_to_set, new_value)
        except Exception as e:
            print e
    return HttpResponse(json.dumps({"msg": "I'm not a useful return..."}), content_type='application/json', status=200)


def save_settings(request):
    if request.method == "POST":
        if request.POST["email"]:
            email = request.POST["email"]
            user = request.user
            user.email = email
            user.save()
        if request.POST["new_password1"] and request.POST["new_password2"] and request.POST["old_password"]:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                try:
                    form.save()
                except Exception, e:
                    print e
    return redirect("auth.views.account_settings")