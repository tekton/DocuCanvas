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
            account.user = User.objects.get(pk=user.id)
            account.created_by = user
            account.save()
            #
            return render_to_response("projects/project_form.html", {}, context_instance=RequestContext(request))
            #response = redirect('auth.views.register')
            #return response
        else:
            print "errors in registration"
            print form.errors

    else:
        print "not post"
        form = RegisterForm()
        next = request.GET.get("next", "/")
        # Add CSRF context token to response.
        return render_to_response("registration/registration.html", {'form': form, 'next': next}, context_instance=RequestContext(request))
    #return render_to_response("registration/registration.html", {'r_form': form, 'next': next}, context_instance=RequestContext(request))


def login_func(request):
    next = request.POST.get("next", "/")
    state = ""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    state = "You're successfully logged in!"
                else:
                    state = "Your account is not active, please contact the site admin."
            else:
                state = "Your username and/or password were incorrect."
            login(request, user)
            return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))
        else:
            #to_json = {"error": "error with username and/or password"}
            #return HttpResponse(simplejson.dumps(to_json), mimetype='application/json', status=400)
            return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))
    else:
        form = AuthenticationForm()

    return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))
