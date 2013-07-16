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
from socialplatform.models import TwitterProfile, FacebookProfile

from django.utils import simplejson

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
    next = request.GET.get("next", "/")
    state = ""
    stateStatus = ""
    if request.method == 'POST':
	next = request.POST.get("next", "/")  # in theory we could take the default from before, but in case a url gets weird lets set a real default
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
                return redirect(next)
            else:
                #to_json = {"error": "error with username and/or password"}
                #return HttpResponse(simplejson.dumps(to_json), mimetype='application/json', status=400)
                state = "Your username and/or password were incorrect."
                return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))
        except Exception, e:
            print "Error authenticating form"
            print e

    else:
        form = AuthenticationForm()

    return render_to_response("registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))

@login_required
def account_settings(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        twat = TwitterProfile.objects.get(user=request.user)
    except Exception, e:
        twat = TwitterProfile(user=request.user, user_name='admin', active=False)
        print e
    try:
        fb = FacebookProfile.objects.get(user=request.user)
    except Exception, e:
        fb = FacebookProfile(active=False)
        raise e
    return render_to_response("registration/account_settings.html", {"projects": projects, "tw": twat, "fb": fb}, context_instance=RequestContext(request))

@login_required
def change_password(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

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
                return render_to_response("registration/change_password.html", {'form': form, "projects": projects}, context_instance=RequestContext(request))
        except Exception, e:
            print "Error validating password"
            print e
    else:
        form = EditAccountForm(SetPasswordForm)
    return render_to_response("registration/change_password.html", {'form': form, "projects": projects}, context_instance=RequestContext(request))

@login_required
def change_email(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

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
    return render_to_response("registration/change_email.html", {'form': form, "projects": projects}, context_instance=RequestContext(request))

@login_required
def user_overview(request, user_id):
    try:
        gadget_user = User.objects.get(pk=user_id)
        issues = Issue.objects.filter(assigned_to=gadget_user).order_by('-project')
        issue_status_updates = IssueStatusUpdate.objects.filter(user=gadget_user).order_by('-time_stamp')
    except Exception, e:
        print e

    return render_to_response("user/user_overview.html", {
        "gadget_user": gadget_user,
        "issues": issues,
        "status_updates": issue_status_updates,
        }, context_instance=RequestContext(request))
