from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.db.models import Q

from issues.models import Issue, IssueComment, SubscriptionToIssue, PinIssue, MetaIssue, IssueToIssue
from projects.models import Project
from issues.forms import IssueForm, IssueFullForm, CommentForm, AdvSearchForm, MetaIssueForm


@login_required
def pin(request, issue_id):
    to_json = {'success': True, 'is_pinned': False, 'error': False}
    try:
        issue = Issue.objects.get(pk=issue_id)
    except Issue.DoesNotExist:
        raise Http404

    try:
        pin = PinIssue.objects.get(user=request.user, issue=issue)
    except PinIssue.DoesNotExist:
        pin = None

    if pin:
        try:
            pin.delete()
        except Exception as e:
            to_json['success'] = False
            to_json['error'] = str(e)
            print e
    else:
        pin = PinIssue()
        pin.issue = issue
        pin.user = request.user
        try:
            pin.save()
        except Exception as e:
            to_json['success'] = False
            to_json['error'] = str(e)
            print e
        else:
            to_json['is_pinned'] = True

    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


@login_required
def assign(request, issue_id, user_id=-1):
    to_json = {'success': True, 'error': False, 'assigned_to': False}
    try:
        issue = Issue.objects.get(pk=issue_id)
    except Issue.DoesNotExist:
        raise Http404

    if user_id == -1:
        if issue.assigned_to == request.user:
            issue.assigned_to = None
            to_json['assigned_to'] = 'none'
        else:
            issue.assigned_to = request.user
            to_json['assigned_to'] = 'self'
    else:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

        if issue.assigned_to == user:
            # this is a no-op
            issue.assigned_to = None
            to_json['assigned_to'] = 'none'
        else:
            issue.assigned_to = user
            if user == request.user:
                to_json['assigned_to'] = 'self'
            else:
                # TODO: report the name of the user being assigned to instead
                to_json['assigned_to'] = 'user'

    if issue:
        try:
            issue.save()
        except Exception as e:
            to_json['success'] = False
            to_json['error'] = str(e)
            to_json['assigned_to'] = False
            print e

    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


@login_required
def subscribe(request, issue_id):
    to_json = {'success': True, 'is_subscribed': False, 'error': False}
    try:
        issue = Issue.objects.get(pk=issue_id)
    except Issue.DoesNotExist:
        raise Http404

    try:
        subscription = SubscriptionToIssue.objects.get(user=request.user, issue=issue)
    except SubscriptionToIssue.DoesNotExist:
        subscription = None

    if subscription:
        try:
            subscription.delete()
        except Exception as e:
            to_json['success'] = False
            to_json['error'] = str(e)
            print e
    else:
        subscription = SubscriptionToIssue()
        subscription.issue = issue
        subscription.user = request.user
        try:
            subscription.save()
        except Exception as e:
            to_json['success'] = False
            to_json['error'] = str(e)
            print e
        else:
            to_json['is_subscribed'] = True

    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


@login_required
def set_bug_state(request):
    to_json = {}
    print 'trying to set bug state'
    print request.POST['issue']
    print request.POST['status']
    try:
        issue = Issue.objects.get(pk=request.POST['issue'])
        issue.status = request.POST['status']
        issue.save()
        to_json["status"] = "Bug status set"
        if request.POST['status'] == 'fixed':
            return submit_comment(request, issue.id)
    except:
        to_json["status"] = "Unable to set bug state"
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


@login_required
def issue_to_issue_link(request):
    to_json = {}

    print request.POST['primary_issue']
    print request.POST['secondary_issue']
    print request.POST['link_type']

    if request.POST['primary_issue'] == request.POST['secondary_issue']:
        to_json['response'] = 'An issue cannot be related to itself'

    else:
        try:
            primary_issue = Issue.objects.get(pk=request.POST['primary_issue'])

            try:
                secondary_issue = Issue.objects.get(pk=request.POST['secondary_issue'])

                try:
                    issue_to_issue_link = IssueToIssue.objects.get(primary_issue=primary_issue, secondary_issue=secondary_issue)
                    if issue_to_issue_link.link_type == request.POST['link_type']:
                        to_json['response'] = 'Link already exists'

                    else:
                        old_link_type = issue_to_issue_link.link_type
                        issue_to_issue_link.link_type = request.POST['link_type']
                        issue_to_issue_link.save()

                        if request.POST['link_type'] == 'duplicate':
                            primary_issue.status = request.POST['link_type']
                            primary_issue.save()

                        to_json['response'] = 'Changed old link from ' + str(old_link_type) + ' to ' + str(request.POST['link_type'])

                except Exception, e:
                    issue_to_issue_link = IssueToIssue()
                    issue_to_issue_link.primary_issue = primary_issue
                    issue_to_issue_link.secondary_issue = secondary_issue
                    issue_to_issue_link.link_type = request.POST['link_type']
                    issue_to_issue_link.save()

                    if request.POST['link_type'] == 'duplicate':
                        primary_issue.status = request.POST['link_type']
                        primary_issue.save()

                    to_json['response'] = 'Linked Issue: ' + str(request.POST['primary_issue']) + ' to Issue: ' + str(request.POST['secondary_issue']) + ' as ' + str(request.POST['link_type'])

            except Exception, e:
                print e
                to_json['response'] = 'Cannot find Secondary Issue'
        except Exception, e:
            print e
            print 'cannot find primary issue'
            to_json['response'] = 'Cannot find Primary Issue'

    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')


@login_required
def meta_issue_form(request, issue_id=-1):
    if request.method == "GET":
        if issue_id == -1:
            return render_to_response('issues/meta_issue_form.html', {'form': MetaIssueForm(), 'new': True}, context_instance=RequestContext(request))

        try:
            mi = MetaIssue.objects.get(pk=issue_id)
        except MetaIssue.DoesNotExist:
            raise Http404

        return render_to_response('issues/meta_issue_form.html', {'form': MetaIssueForm(instance=mi), 'new': False}, context_instance=RequestContext(request))
    else:
        if issue_id != -1:
            try:
                mi = MetaIssue.objects.get(pk=issue_id)
            except MetaIssue.DoesNotExist:
                raise Http404
            form = MetaIssueForm(data=request.POST, instance=mi)
        else:
            form = MetaIssueForm(data=request.POST)

        if form.is_valid():
            try:
                mi = form.save()
            except Exception as e:
                print e
                raise e

            if form.instance:
                return redirect('issues.views.meta_issue_form', mi.id)
            else:
                return redirect('issues.views.meta_issue_form')

        else:
            return render_to_response('issues/meta_issue_form.html', {'form': form, 'new': form.instance is None}, context_instance=RequestContext(request))


@login_required
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
                return redirect('issues.views.issue_overview', issue.id)
            else:
                return render_to_response('issues/issue_form.html', {'form': form}, context_instance=RequestContext(request))

    else:
        form = IssueForm()
        try:
            projects = Project.objects.all()
        except:
            print 'Unable to grab all projects'
    return render_to_response("issues/issue_form.html", {'form': form, "projects": projects, "page_type": "Issue", "page_value": "New"}, context_instance=RequestContext(request))


@login_required
def issue_form_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        projects = Project.objects.all()
        form = IssueForm(initial={"project": project}, auto_id=False)
    except:
        print "Unable to find associated project"
        form = IssueForm()
    return render_to_response("issues/issue_form_project.html", {'form': form, 'project': project, 'page_type': project.name, 'page_value': "Issue", 'projects': projects}, context_instance=RequestContext(request))

@login_required
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
        print 'Unable to find subscription for issue'
        subscribe = None

    try:
        comment_form = CommentForm()
    except Exception, e:
        print e

    form = IssueFullForm(instance=issue)

    return render_to_response("issues/issue_overview.html", {'issue': issue, 'pin': pin, 'subscribe': subscribe, 'form': form, 'comment_form': comment_form, 'comments': comments, "users": users, "projects": projects, "page_type": issue.project.name, "page_value": "Issue"}, context_instance=RequestContext(request))


@login_required
def edit(request, issue_id):
    if request.method == 'POST':
        issue = Issue.objects.get(pk=issue_id)
        form = IssueFullForm(request.POST, instance=issue)
        if form.is_valid():
            try:
                issue = form.save()
            except Exception, e:
                print e
                print form.errors
            if issue.id:
                return redirect('issues.views.issue_overview', issue.id)
            else:
                return render_to_response('issues/issue_edit.html', {'form': form, "issue": issue}, context_instance=RequestContext(request))

    else:
        issue = Issue.objects.get(pk=issue_id)
        form = IssueFullForm(instance=issue,initial={"project": issue.project}, auto_id=False)
    return render_to_response("issues/issue_edit.html", {"form": form, "issue": issue, "page_type": "Edit", "page_value": issue.title}, context_instance=RequestContext(request))


@login_required
def issue_search_simple(request):
    if request.method == "GET":
        return render_to_response("issues/issue_adv_search.html", context_instance=RequestContext(request))

    search = request.POST['searchText']
    print search

    q = Issue.objects.filter(Q(summary__contains=search) | Q(description__contains=search))
    return render_to_response("issues/issue_search_results.html", {'results': q}, context_instance=RequestContext(request))


@login_required
def issue_search_advanced(request):
    if request.method == "GET":
        return render_to_response("issues/issue_adv_search.html", {'form': AdvSearchForm()}, context_instance=RequestContext(request))

    form = AdvSearchForm(request.POST)
    if not form.is_valid():
        raise Exception("Invalid adv search form values")

    query = None

    for field in form.cleaned_data.keys():
        qr = None
        if len(form.cleaned_data[field]) == 0:
            continue
        for item in form.cleaned_data[field]:
            q = Q(**{"%s__contains" % field: item}) if type(item) == unicode else Q(**{"%s" % field: item})
            if qr:
                qr = qr | q
            else:
                qr = q
        if query:
            query = query & qr
        else:
            query = qr

    results = Issue.objects.filter(query)
    return render_to_response("issues/issue_search_results.html", {'results': results}, context_instance=RequestContext(request))


@login_required
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
    return redirect('issues.views.issue_overview', issue_id, permanent=False)


@login_required
def unassigned_issues(request):
    q = Issue.objects.filter(Q(assigned_to__isnull = True) & (Q(status = "active") | Q(status = "retest") | Q(status = "unverified") | Q(status__isnull=True)))
    return render_to_response('issues/issue_unassigned.html', {'issues': q}, context_instance=RequestContext(request))
