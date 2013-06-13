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
                return render_to_response("theme/registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))
        except Exception, e:
            print "Error authenticating form"
            print e

    else:
        form = AuthenticationForm()

    return render_to_response("theme/default/registration/login.html", {'a_form': form, 'next': next, 'state': state}, context_instance=RequestContext(request))


def account_settings(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    return render_to_response("registration/account_settings.html", {"projects": projects}, context_instance=RequestContext(request))


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
    try:
        gadget_user = User.objects.get(pk=user_id)
        #issues = Issue.objects.filter(assigned_to=gadget_user).order_by('-created')
        issues = Issue.objects.filter(assigned_to=gadget_user).order_by('-project')
        issue_status_updates = IssueStatusUpdate.objects.filter(user=gadget_user).order_by('-time_stamp')

        blank_issues = issues.filter(status=None)
        not_a_bug_issues = issues.filter(status='not_a_bug')
        wont_fix_issues = issues.filter(status='wont_fix')
        duplicate_issues = issues.filter(status='duplicate')
        active_issues = issues.filter(status='active')
        fixed_issues = issues.filter(status='fixed')
        retest_issues = issues.filter(status='retest')
        unverified_issues = issues.filter(status='unverified')

        blank_count = blank_issues.count()
        not_a_bug_count = not_a_bug_issues.count()
        wont_fix_count = wont_fix_issues.count()
        duplicate_count = duplicate_issues.count()
        active_count = active_issues.count()
        fixed_count = fixed_issues.count()
        retest_count = retest_issues.count()
        unverified_count = unverified_issues.count()

        #assignment count by project
        projects = Project.objects.all()
        project_dict = {}
        for project in projects:
            temp_dict = {}
            project_issues = Issue.objects.filter(project=project, assigned_to=gadget_user)
            for issue in project_issues:
                temp_dict[issue.id] = issue.summary
            temp_dict[project.name] = Issue.objects.filter(project=project, assigned_to=gadget_user).count()
            project_dict[project.name] = temp_dict
            #project_dict[project.name] = Issue.objects.filter(project=project, assigned_to=gadget_user).count()

        project_array = []

        project_list = []
        issue_list = []
        for project in projects:

            # List of Projects
            project_data = {}
            project_data["id"] = project.id
            project_data["name"] = project.name
            project_list.append(project_data)

            project_info = {}
            project_info["name"] = project.name
            project_info["issues"] = []

            project_issues = Issue.objects.filter(project=project, assigned_to=gadget_user)
            for issue in project_issues:
                issue_info = {}
                issue_info["id"] = issue.id
                issue_info["summary"] = issue.summary
                issue_info["status"] = issue.status
                issue_info["project"] = issue.project.name

                project_info["issues"].append(issue_info)

            project_array.append(project_info)

        project_json = simplejson.dumps(project_array)

    except Exception, e:
        print e

    return render_to_response("theme/default/user/user_overview.html", {"projectsAsJson": project_json, "gadget_user": gadget_user, "issues": issues, "status_updates": issue_status_updates, "blank_issues": blank_issues, "not_a_bug_issues": not_a_bug_issues, "wont_fix_issues": wont_fix_issues, "duplicate_issues": duplicate_issues, "active_issues": active_issues, "fixed_issues": fixed_issues, "retest_issues": retest_issues, "unverified_issues": unverified_issues ,"project_dict": project_dict , "blank_count": blank_count, "not_a_bug_count": not_a_bug_count, "wont_fix_count": wont_fix_count, "duplicate_count": duplicate_count, "active_count": active_count, "fixed_count": fixed_count, "retest_count": retest_count, "unverified_count": unverified_count, "page_type": gadget_user.username}, context_instance=RequestContext(request))

