
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q

from oauth2client.client import OAuth2WebServerFlow


def _get_flow():
    gSettings = settings.OAUTH_SETTINGS['google']
    return OAuth2WebServerFlow(client_id=gSettings['devKey'], client_secret=gSettings['devSecretKey'], scope='https://www.googleapis.com/auth/userinfo.email', redirect_uri='http://localtest.channelfactory.com:8000/acct/oauth2callback')


def oauth_test(request):
    flow = _get_flow()
    return redirect(flow.step1_get_authorize_url())


def oauth_callback(request):
    if "code" not in request.GET:
        raise Http404
    flow = _get_flow()
    credentials = flow.step2_exchange(request.GET['code'])
    return HttpResponse(credentials.to_json(), mimetype="text/plain")
