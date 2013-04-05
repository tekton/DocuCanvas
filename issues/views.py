# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import *
from issues.models import *
from issues.forms import *


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
        comment_form = CommentForm()
    except:
        print "Somebody messed up the issue overview"
    return render_to_response("issues/issue_overview.html", {'issue_O': issue, 'comment_form_O': comment_form}, context_instance=RequestContext(request))


def submit_comment(request, issue_id):
    """
        Takes a basic comment ModelForm with additional issue_id and user notes added in the form outside the base model form; though those could be added later
    """
    try:
        comment = IssueComment()
        #
        form = CommentForm(request.POST, instance=comment)
        #
        if form.is_valid():
            try:
                comment = form.save()  # save the modelform's model!
            except Exception, e:
                print e
                print form.errors
            if comment.id:
                return issue_overview(request, issue_id)
            else:
                return issue_overview(request, issue_id)
                # return render_to_response("issues/issue_overview.html", {'issue_O': issue, 'comment_form_O': form}, context_instance=RequestContext(request))
        else:
            print form
            print form.errors
            return issue_overview(request, issue_id)
            # return render_to_response("issues/issue_overview.html", {'issue_O': issue, 'comment_form_O': form}, context_instance=RequestContext(request))
    except Exception, e:
        print e

    return issue_overview(request, issue_id)
