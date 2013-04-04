from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from forms import RegisterForm
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.core.mail import get_connection
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.models import *

def register(request):
    '''
    if request.method == 'POST':
        next = request.POST.get("next", "/")
        form = RegisterForm(request.POST)
        if form.is_valid():
            # new_user = form.save()
            try:
                form.save()
            except:
                print "Unable to save form..."
                return render_to_response("registration/registration.html", {'form': form, 'next': next}, context_instance=RequestContext(request))
            # log the user in before sending them to their next destination
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password1"))
            login(request, user)
            ### TODO Create account here!
            account = Account()
            account.created_by = user
            account.original_splash_page = request.session.get('splash')
            account.save()
            #
            if request.POST.get("video", False) is not False:
                print "go to new campaign straight away!"
                response = redirect('campaign.views.new_campaign')
                print request.POST.get("video")
                response["Location"] += "?video=" + str(request.POST.get("video"))
            else:
                print "there was no video posted, so just go to the url for new url"
                response = redirect('campaign.views.campaign_url')
            return response
        else:
            print "errors in registration"
            print form.errors

    else:
    '''
        
    print "not post"
    form = RegisterForm()
    next = request.GET.get("next", "/")
    # Add CSRF context token to response.
    return render_to_response("registration/registration.html", {'form': form, 'next': next}, context_instance=RequestContext(request))
    #return render_to_response("registration/registration.html", {'r_form': form, 'next': next}, context_instance=RequestContext(request))