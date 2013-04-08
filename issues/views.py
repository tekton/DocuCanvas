# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# from projects.models import Project
from issues.models import Issue, IssueComment
from issues.forms import IssueForm, CommentForm
from django.contrib.auth.models import User


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
        form = IssueForm()
        # projects = Project()
        print form
    return render_to_response("issues/issue_form.html", {'form': form}, context_instance=RequestContext(request))


def issue_overview(request, issue_id):
    try:
        issue = Issue.objects.get(pk=issue_id)
        comments = IssueComment.objects.filter(issue=issue).order_by('-created')
    except Exception, e:
        print "Somebody messed up the issue overview"
        print e

    try:
        comment_form = CommentForm()
    except Exception, e:
        print e

    return render_to_response("issues/issue_overview.html", {'issue': issue, 'comment_form': comment_form, 'comments':  comments, "page_type":"Issue"}, context_instance=RequestContext(request))


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
