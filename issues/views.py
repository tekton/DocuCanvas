# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from django.db import models
from django.db.models import Q
# from projects.models import Project
from issues.models import Issue, IssueComment, SubscriptionToIssue, PinIssue
from projects.models import Project
from issues.forms import IssueForm, CommentForm
from django.contrib.auth.models import User


def pin(request):
    to_json = {}
    try:
        issue = Issue.objects.get(pk=request.POST['issue'])
        try:
            pin = PinIssue.objects.get(user=request.user, issue=issue)
            pin.delete()
            to_json["status"] = "Unpinning Issue"
        except:
            try:
                pin = PinIssue()
                pin.issue = issue
                pin.user = request.user
                pin.save()
                to_json["status"] = "Successfully pinned issue"
            except Exception, e:
                print e
                to_json["status"] = "Error pinning"
    except:
        to_json["status"] = "Issue does not exist"
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


def assign(request):
    to_json = {}
    try:
        issue = Issue.objects.get(pk=request.POST['issue'])

        if issue.assigned_to == request.user and request.POST['assign'] == 'assign':
            issue.assigned_to = None
            to_json["status"] = "Successfully unassigned issue"
        else:
            if issue.assigned_to:
                to_json["status"] = "Successfully reassigned issue"

            else:
                to_json["status"] = "Successfully assigned issue"

            if request.POST['assign'] == 'assign':
                issue.assigned_to = request.user
            else:
                try:
                    issue.assigned_to = User.objects.get(pk=request.POST['user'])
                except:
                    to_json["status"] = "Unable to find user"

        issue.save()
    except:
        to_json["status"] = "Unable to assign to issue"
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


def subscribe(request):
    to_json = {}
    try:
        issue = Issue.objects.get(pk=request.POST['issue'])
        try:
            subscription = SubscriptionToIssue.objects.get(user=request.user, issue=issue)
            subscription.delete()
            to_json["status"] = "Unsubscribing Issue"
        except:
            try:
                subscription = SubscriptionToIssue()
                subscription.issue = issue
                subscription.user = request.user
                subscription.save()
                to_json["status"] = "Successfully subscribed to Issue"
            except Exception, e:
                print e
                to_json["status"] = "Error subscribing to issue"
    except:
        to_json["status"] = "Issue does not exist"
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


def issue_form(request):
    if request.method == 'POST':
        issue = Issue()
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            try:
                issue = form.save()
            except Exception, e:
                print e
                print form.errors
            if issue.id:
                return redirect('issues.views.issue_overview', issue.id, permanent=True)
            else:
                return render_to_response('issues/issue_form.html', {'form': form}, context_instance=RequestContext(request))
    else:
        project_id = request.GET.get('project')

        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
                form = IssueForm(initial={"project": project}, auto_id=False)
            except:
                print "Unable to find associated project"
        else:
            form = IssueForm()
    return render_to_response("issues/issue_form.html", {'form': form}, context_instance=RequestContext(request))


def issue_overview(request, issue_id):
    try:
        issue = Issue.objects.get(pk=issue_id)
        comments = IssueComment.objects.filter(issue=issue).order_by('-created')
    except Exception, e:
        print "Somebody messed up the issue overview"
        print e

    try:
        users = User.objects.all()
    except Exception, e:
        print "Unable to get user list"
        print e

    try:
        projects = Project.objects.all().order_by('-created')
    except Exception, e:
        print 'Unable to load projects'

    try:
        pin = PinIssue.objects.get(issue=issue, user=request.user)
    except:
        print 'Unable to find pin for issue'
        pin = None

    try:
        subscribe = SubscriptionToIssue.objects.get(issue=issue, user=request.user)
    except:
        print 'Unable to find subsription for issue'
        subscribe = None

    try:
        comment_form = CommentForm()
    except Exception, e:
        print e

    return render_to_response("issues/issue_overview.html", {'issue': issue, 'pin': pin, 'subscribe': subscribe, 'comment_form': comment_form, 'comments': comments, "users": users, "page_type": "Issue", "projects": projects}, context_instance=RequestContext(request))


def issue_search_simple(request):
    if request.method == "GET":
        return redirect('issues.views.issue_overview')

    search = request.POST['searchText']
    print search

    q = Issue.objects.filter(Q(summary__contains=search) | Q(description__contains=search))
    return render_to_response("issues/issue_search_results.html", {'results': q}, context_instance=RequestContext(request))


def submit_comment(request, issue_id):
    """
        Bad assumption: will only be called with POST...
        Takes a basic comment ModelForm with additional issue_id and user notes added in the form outside the base model form; though those could be added later
    """
    try:
        issue = Issue.objects.get(pk=issue_id)
    except Exception, e:
        print "error getting issue"
        raise e

    try:
        comments = IssueComment.objects.filter(issue=issue).order_by('-created')
    except Exception, e:
        print "Error getting comments"
        raise e

    comment = IssueComment()

    if request.method == 'POST':
        try:
            #
            form = CommentForm(request.POST, instance=comment)
            #
            if form.is_valid():
                try:
                    comment = form.save()  # save the modelform's model!
                except Exception, e:
                    print "Error saving form"
                    print e
                    print form.errors
            else:
                print "comment form not valid"
                print form
                print form.errors
        except Exception, e:
            print "Error somewhere in comment posting"
            print e
            # form = CommentForm(user=User, issue=issue)
            form = CommentForm()
    else:
        # form = CommentForm(user=User, issue=issue)
        form = CommentForm()
    return render_to_response("issues/issue_overview.html", {'issue': issue, 'comment_form': form, 'comments':  comments}, context_instance=RequestContext(request))
