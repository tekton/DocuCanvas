# Create your views here.
import urllib

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from facebook.models import Facebook


def facebook_login(request):
	# First step of process, redirects user to facebook, which redirects to authentication_callback.
    args = {
        'client_id': '441109929301348',
        'scope': 'email',
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))
