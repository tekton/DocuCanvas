from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from forms import RegisterForm, EditAccountForm, ChangeEmailForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.core.mail import get_connection
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from accounts.models import *
from issues.models import *


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
            return redirect(next)
        else:
            print "errors in registration"
            print form.errors

    else:
        form = RegisterForm()
        next = request.GET.get("next", "/")
     # Add CSRF context token to response.
    # return render_to_response("registration/registration.html", {'form': form, 'next': next}, context_instance=RequestContext(request))
    # return render_to_response("registration/registration.html", {'r_form': form, 'next': next}, context_instance=RequestContext(request))
    return render_to_response("registration/login.html", {}, context_instance=RequestContext(request))


def login_func(request):
    next = request.POST.get("next", "/")
    state = ""
    if request.method == 'POST':
        try:
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
                #return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))
                return redirect('dashboard.views.home')
            else:
                #to_json = {"error": "error with username and/or password"}
                #return HttpResponse(simplejson.dumps(to_json), mimetype='application/json', status=400)
                return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))
        except Exception, e:
            print "Error authenticating form"
            print e

    else:
        form = AuthenticationForm()

    return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))


def account_settings(request):
    return render_to_response("registration/account_settings.html", {}, context_instance=RequestContext(request))


def change_password(request):
    if request.method == "POST":
        try:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                try:
                    form.save()
                    return redirect('dashboard.views.home')
                except Exception, e:
                    print "Error saving form"
            else:
                return render_to_response("registration/change_password.html", {'form': form}, context_instance=RequestContext(request))
        except Exception, e:
            print "Error validating password"
            print e
    else:
        form = EditAccountForm(SetPasswordForm)
    return render_to_response("registration/change_password.html", {'form': form}, context_instance=RequestContext(request))


def change_email(request):
    if request.method == "POST":
        try:
            form = ChangeEmailForm(data=request.POST)
            if form.is_valid():
                try:
                    user = request.user
                    user.email = request.POST['email']
                    user.save()
                    return redirect('dashboard.views.home')
                except Exception, e:
                    print e

            else:
                print "form not valid"
        except Exception, e:
            print "Error getting email from database"
            print e
    else:
        form = ChangeEmailForm()
    return render_to_response("registration/change_email.html", {'form': form}, context_instance=RequestContext(request))


def user_overview(request, user_id):
    gadget_user = User.objects.get(pk=user_id)
    issues = Issue.objects.filter(assigned_to=gadget_user).order_by('-created')
    return render_to_response("user/user_overview.html", {"gadget_user": gadget_user, "issues": issues, "page_type": gadget_user.username}, context_instance=RequestContext(request))
