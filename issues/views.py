import json
import hashlib
import pickle
import types

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.db.models import Count
from django.forms.models import model_to_dict
# mail
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.template.loader import get_template
# /mail
from accounts.forms import PermissionForm
from accounts.utils import get_permission_form_for_model, set_permissions_for_model

from datetime import date
from datetime import datetime

from issues.models import Issue, IssueComment, SubscriptionToIssue, PinIssue, MetaIssue, IssueToIssue, IssueStatusUpdate, IssueFieldUpdate, IssueHistorical, IssueScreenshot, AdvancedSearchHash, TrackerHash
from accounts import utils as rputils
from accounts.models import Account
from accounts.views import cache_checkUserTemplate
from projects.models import Project
from issues.forms import IssueForm, IssueFullForm, CommentForm, AdvSearchForm, MetaIssueForm, TestForm
from communications.views import prepMail
from sprints.models import Sprint

import celery
import traceback


@login_required
def pin(request, issue_id):
    if request.is_ajax():
        to_json = {'success': True, 'is_pinned': False, 'error': False}
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            to_json['success'] = False
            to_json['error'] = str(e)

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
        else:
            pin = PinIssue()
            pin.issue = issue
            pin.user = request.user
            try:
                pin.save()
            except Exception as e:
                to_json['success'] = False
                to_json['error'] = str(e)
            else:
                to_json['is_pinned'] = True
        return HttpResponse(json.dumps(to_json), mimetype='application/json')
    else:
        return redirect('issues.views.issue_overview', issue_id)


@login_required
def issueSubscribe(request, issue_id, user_id):
    rtn_dict = {"success": True}
    u = None
    issue = None
    
    try:
        u = User.objects.get(pk=user_id)
    except Exception as e:
        rtn_dict = {"error": "Unable to get User", "no_user_e": str(e), "success": False}
    try:
        issue = Issue.objects.get(pk=issue_id)
    except Exception as e:
        rtn_dict = {"error": "Unable to get Issue", "no_issue_e": str(e), "success": False}

    try:
        sub = SubscriptionToIssue.objects.get(user=u, issue=issue)
    except:
        sub = SubscriptionToIssue()
    if u and issue:
        sub.user = u
        sub.issue = issue
        try:
            sub.save()
        except Exception as e:
            rtn_dict = {"error": "Unable to save Subscription", "no_save_e": str(e), "success": False}
    else:
        pass
    return HttpResponse(json.dumps(rtn_dict), content_type='application/json')


@login_required
@permission_required("issues.change_issue", raise_exception=True)
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
            issue.save(request.user)
            # TODO - send mail to the newly assigned! and all the other people...
        except Exception as e:
            print "Unable to save issue"
            to_json['success'] = False
            to_json['error'] = str(e)
            to_json['assigned_to'] = False
            print e

    if request.is_ajax():
        return HttpResponse(json.dumps(to_json), mimetype='application/json')
    else:
        return redirect('issues.views.issue_overview', issue_id)


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

    if request.is_ajax():
        return HttpResponse(json.dumps(to_json), mimetype='application/json')
    else:
        return redirect('issues.views.issue_overview', issue_id)


@login_required
@permission_required("issues.change_issue", raise_exception=True)
def set_bug_state(request):
    to_json = {}

    try:
        issue = Issue.objects.get(pk=request.POST['issue'])
        old_status = issue.status
        issue.status = request.POST['status']
        issue.save(request.user)
        to_json["status"] = "Bug status set"
        if request.POST['status'] == 'fixed':
            return submit_comment(request, issue.id)
    except Exception, e:
        print e
        to_json["status"] = "Unable to set bug state"
    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
def unlink_issues(request):
    to_json = {}
    status_code = 200

    try:
        primary_issue = Issue.objects.get(pk=request.POST['primary_issue'])
        try:
            secondary_issue = Issue.objects.get(pk=request.POST['secondary_issue'])

            try:
                issue_to_issue_link = IssueToIssue.objects.get(primary_issue=primary_issue, secondary_issue=secondary_issue)
                issue_to_issue_link.delete()
                if primary_issue.status == 'duplicate':
                    primary_issue.status = None
                    primary_issue.save(request.user)
                status_code = 200
                to_json['response'] = 'Unlinked Issue ' + str(request.POST['primary_issue']) + ' and Issue ' + str(request.POST['secondary_issue'])

            except Exception, e:
                print e
                status_code = 400
                to_json['response'] = 'Unable to find Issue to Issue Link'

        except Exception, e:
            print e
            status_code = 400
            to_json['response'] = 'Cannot find Secondary Issue'
    except Exception, e:
        print e
        print 'cannot find primary issue'
        status_code = 400
        to_json['response'] = 'Cannot find Primary Issue'
    return HttpResponse(json.dumps(to_json), mimetype='application/json', status=status_code)


@login_required
@permission_required("issues.change_issue", raise_exception=True)
def issue_to_issue_link(request):
    to_json = {}

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
                            primary_issue.save(request.user)
                            #secondary_issue.status = request.POST['link_type']
                            #secondary_issue.save(request.user)

                        to_json['response'] = 'Changed old link from ' + str(old_link_type) + ' to ' + str(request.POST['link_type'])

                except Exception, e:
                    issue_to_issue_link = IssueToIssue()
                    issue_to_issue_link.primary_issue = primary_issue
                    issue_to_issue_link.secondary_issue = secondary_issue
                    issue_to_issue_link.link_type = request.POST['link_type']
                    issue_to_issue_link.save()

                    if request.POST['link_type'] == 'duplicate':
                        primary_issue.status = request.POST['link_type']
                        primary_issue.save(request.user)
                        #secondary_issue.status = request.POST['link_type']
                        #secondary_issue.save(request.user)

                    to_json['response'] = 'Linked Issue: ' + str(request.POST['primary_issue']) + ' to Issue: ' + str(request.POST['secondary_issue']) + ' as ' + str(request.POST['link_type'])

            except Exception, e:
                print e
                to_json['response'] = 'Cannot find Secondary Issue'
        except Exception, e:
            print e
            print 'cannot find primary issue'
            to_json['response'] = 'Cannot find Primary Issue'

    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
def meta_issue_form(request, issue_id=-1):
    projects = Project.objects.all()
    print "meta issue"

    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
        projects = []

    if request.method == "GET":
        if issue_id == -1:
            if not request.user.has_perm("issues.add_metaissue"):
                raise PermissionDenied

            return render_to_response('issues/meta_issue_wizard.html', {'form': MetaIssueForm(), 'new': True, 'pform': PermissionForm(), "projects": projects}, context_instance=RequestContext(request))

        try:
            mi = MetaIssue.objects.get(pk=issue_id)
        except MetaIssue.DoesNotExist:
            raise Http404

        pv, pu, pd = rputils.user_permissions(request.user, mi)
        if not request.user.has_perm("issues.change_metaissue") or not pv or not pu:
            raise PermissionDenied

        return render_to_response('issues/meta_issue_form.html', {'form': MetaIssueForm(instance=mi), 'new': False, 'canDelete': pd, 'pform': get_permission_form_for_model(mi), "projects": projects}, context_instance=RequestContext(request))

    else:
        if issue_id != -1:
            try:
                mi = MetaIssue.objects.get(pk=issue_id)
            except MetaIssue.DoesNotExist:
                raise Http404

            if not request.user.has_perm("issues.change_metaissue") or not rputils.user_can_update(request.user, mi):
                raise PermissionDenied
            form = MetaIssueForm(data=request.POST, instance=mi)
            pform = PermissionForm(data=request.POST)
            print form
            print form.errors
        else:
            if not request.user.has_perm("issues.add_metaissue"):
                raise PermissionDenied
            form = MetaIssueForm(data=request.POST)
            pform = PermissionForm(data=request.POST)

        if form.is_valid():
            try:
                mi = form.save()
                if pform.is_valid():
                    set_permissions_for_model(mi, view_users=pform.cleaned_data['view_users'], update_users=pform.cleaned_data['update_users'], delete_users=pform.cleaned_data['update_users'])
            except Exception as e:
                print e
                raise e

            if form.instance:
                return redirect('issues.views.meta_issue_overview', mi.id)
            else:
                return redirect('issues.views.meta_issue_form')

        else:
            return render_to_response('issues/meta_issue_form.html', {'form': form, 'new': True, 'pform': pform, "projects": projects}, context_instance=RequestContext(request))


@login_required
def meta_issue_overview(request, meta_issue_id):
    try:
        meta_issue = MetaIssue.objects.get(pk=meta_issue_id)
    except:
        # TODO error out to a specific page or message
        meta_issue = MetaIssue()

    issues = Issue.objects.filter(meta_issues=meta_issue)
    issues_active = issues.filter((Q(status='active') | Q(status='unverified') | Q(status=None) | Q(status="Retest")))
    issues_non_active = issues.filter((~Q(status='active') & ~Q(status='unverified') & ~Q(status=None) & ~Q(status="Retest")))

    issue_counts = Issue.objects.filter(meta_issues=meta_issue).values("status").annotate(Count("id")).order_by("status")
    print issue_counts

    print issues
    print issues_active
    print issues_non_active

    try:
        projects = Project.objects.all()
    except:
        projects = []

    return render_to_response('issues/meta_issue_overview.html', {"metaissue": meta_issue,
                                                                  "projects": projects,
                                                                  "issues": issues_active,
                                                                  "issues_non_active": issues_non_active,
                                                                  "issue_counts": issue_counts,
        }, context_instance=RequestContext(request))


@login_required
def meta_issue_stats(request, meta_issue_id):
    try:
        meta_issue = MetaIssue.objects.get(pk=meta_issue_id)

        issues = Issue.objects.filter(meta_issues=meta_issue)

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

        issues_active = issues.filter((Q(status='active') | Q(status='unverified') | Q(status=None) | Q(status="retest")))
        criticality_issues = Issue.objects.filter(Q(meta_issues=meta_issue) & (Q(status='active') | Q(status='unverified') | Q(status='duplicate'))).order_by('-criticality')
        bugs_for_review = Issue.objects.filter(Q(meta_issues=meta_issue) & (Q(status='wont_fix') | Q(status='not_a_bug') | Q(status='retest')))
    except Exception, e:
        print e

    return render_to_response('issues/meta_issue_stats.html', {"criticality_issues": criticality_issues,
                                                               "bugs_for_review": bugs_for_review,
                                                               "blank_issues": blank_issues,
                                                               "not_a_bug_issues": not_a_bug_issues,
                                                               "wont_fix_issues": wont_fix_issues,
                                                               "duplicate_issues": duplicate_issues,
                                                               "active_issues": active_issues,
                                                               "fixed_issues": fixed_issues,
                                                               "retest_issues": retest_issues,
                                                               "unverified_issues": unverified_issues,
                                                               "blank_count": blank_count,
                                                               "not_a_bug_count": not_a_bug_count,
                                                               "wont_fix_count": wont_fix_count,
                                                               "duplicate_count": duplicate_count,
                                                               "active_count": active_count,
                                                               "fixed_count": fixed_count,
                                                               "retest_count": retest_count,
                                                               "unverified_count": unverified_count,
                                                               "page_type": meta_issue.title,
                                                               "issues_active": issues_active,
                                                               "meta_issue": meta_issue,
                                                               "page_value": "Report"}, context_instance=RequestContext(request))


@login_required
@permission_required("issues.add_issue", raise_exception=True)
def issue_form(request):
    try:
        projects = Project.objects.all()
    except Exception as e:
        print 'Unable to grab all projects'
        print str(e)
    if request.method == 'POST':
        issue = Issue()
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            try:
                issue.created_by = request.user
                issue = form.save(request.user)
            except Exception, e:
                print e
                print form.errors

            try:
                issue.created_by = request.user
                issue.save(request.user)
                print "item saved; now try to mail on it"
                prepMail.delay(issue, update_type='created')  # communications/views.py
                # msg.send()  # commented out to avoid spamy spam spam
            except Exception, e:
                print e

            for afile in request.FILES.getlist('myfiles'):
                image = IssueScreenshot(issue=issue, screenshot=afile)
                try:
                    image.save()
                except Exception, e:
                    print e

            if issue.id:
                return redirect('issues.views.issue_overview', issue.id)
            else:
                return render_to_response('issues/issue_form.html', {'form': form}, context_instance=RequestContext(request))
        else:
            print "form not valid"
            print form.errors
    else:
        form = IssueForm()

    return render_to_response("issues/issue_form.html", {'form': form, 
                                                         "projects": projects,
                                                         "page_type": "Issue",
                                                         "page_value": "New",
                                                        }, context_instance=RequestContext(request))


@login_required
@permission_required("issues.change_issue", raise_exception=True)
def issue_form_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        projects = Project.objects.all()
        form = IssueForm(initial={"project": project}, auto_id=False)
    except:
        print "Unable to find associated project"
        form = IssueForm()
    return render_to_response("issues/issue_form_project.html", {'form': form, 
                                                                 'project': project,
                                                                 'page_type': project.name,
                                                                 'page_value': "Issue",
                                                                 'projects': projects,
                                                                }, context_instance=RequestContext(request))


@login_required
@permission_required("issues.change_issue", raise_exception=True)
def issue_form_project_and_meta(request, project_id, meta_id):
    try:
        project = Project.objects.get(pk=project_id)
        meta = MetaIssue.objects.get(pk=meta_id)
        projects = Project.objects.all()
        form = IssueForm(initial={"project": project, "meta_issues": meta}, auto_id=False)
    except:
        print "Unable to find associated project or meta issue"
        form = IssueForm()
    return render_to_response("issues/issue_form_project.html", {'form': form, 'project': project, 'page_type': project.name, 'page_value': "Issue", 'projects': projects}, context_instance=RequestContext(request))


@login_required
def issue_overview(request, issue_id):
    issue = Issue()
    try:
        issue = Issue.objects.get(pk=issue_id)
        comments = IssueComment.objects.filter(issue=issue).order_by('-created')
        images = IssueScreenshot.objects.filter(issue=issue)

        try:
            project_issues = Issue.objects.filter(project=issue.project)
            project_issues = project_issues.exclude(pk=issue.id)
        except Exception, e:
            print "could not find other issues in same project :: {}".format(str(e))
    except Exception, e:
        print "Somebody messed up the issue overview :: {}".format(str(e))

    try:
        users = User.objects.all()
    except Exception, e:
        # print "Unable to get user list :: {}".format(str(e)) # we know what went wrong technically
        pass

    try:
        projects = Project.objects.all().order_by('created')
    except Exception, e:
        # print 'Unable to load projects :: {}'.format(str(e)) # we know what went wrong technically
        pass

    try:
        pin = PinIssue.objects.get(issue=issue, user=request.user)
    except Exception as e:
        # print e  # we know what went wrong technically
        pin = None

    try:
        subscribe = SubscriptionToIssue.objects.get(issue=issue, user=request.user)
    except Exception as e:
        # print e  # we know what went wrong technically
        subscribe = None

    try:
        related_issues = IssueToIssue.objects.select_related().filter(Q(primary_issue=issue) | Q(secondary_issue=issue))
    except:
        # print 'Unable to find any related issues'  # just causes log spam
        pass

    try:
        comment_form = CommentForm()
    except Exception as e:
        print e

    form = IssueFullForm(instance=issue)

    try:
        accounts = Account.objects.all().order_by('user__username')
    except Exception as e:
        print "No accounts for you...or me... :: {}".format(str(e))
    # attempt to get the user defined template first, then check for an override template
    stack = traceback.extract_stack()
    filename, codeline, viewName, text = stack[-1]
    default = "issues/issue_overview.html"
    try:
        cache_template = cache_checkUserTemplate(request.user, viewName)
        if cache_template:
            default = cache_template
    except Exception as e:
        # only print if debug is really necisary
        print "Unable to get template from cache :: ".format(str(e))
        pass
    template = request.GET.get("template", default)
    return render_to_response(template, {'issue': issue,
                                                             'related_issues': related_issues,
                                                             'project_issues': project_issues,
                                                             'pin': pin,
                                                             'subscribe': subscribe,
                                                             'form': form,
                                                             'comment_form': comment_form,
                                                             'comments': comments,
                                                             "users": users,
                                                             "projects": projects,
                                                             "page_type": issue.project.name,
                                                             "page_value": "Issue",
                                                             "images": images,
                                                             'accounts': accounts,
                                                             "users": users,
                                                            }, context_instance=RequestContext(request))


@login_required
@permission_required("issues.change_issue", raise_exception=True)
def edit(request, issue_id):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        sprints = Sprint.objects.all()
    except Exception, e:
        print e

    if request.method == 'POST':
        issue = Issue.objects.get(pk=issue_id)
        form = IssueFullForm(request.POST, instance=issue)
        for afile in request.FILES.getlist('myfiles'):
            image = IssueScreenshot(issue=issue, screenshot=afile)
            try:
                image.save()
            except Exception as e:
                print e

        if form.is_valid():
            try:
                issue.modified_by = request.user
                issue = form.save(request.user)
                print "item saved; now try to mail on it!"
                prepMail.delay(issue)  # communications/views.py
            except Exception, e:
                print e
                print form.errors
            '''
            try:
                print 'editing issue'
                issue.save(request.user)
            except Exception, e:
                print e
            '''
            if issue.id:
                return redirect('issues.views.issue_overview', issue.id)
            else:
                return render_to_response('issues/issue_edit.html', {'form': form, "issue": issue, "projects": projects, 'sprints': sprints}, context_instance=RequestContext(request))

    else:
        issue = Issue.objects.get(pk=issue_id)
        form = IssueFullForm(instance=issue,initial={"project": issue.project}, auto_id=False)
    return render_to_response("issues/issue_edit.html", {"form": form, "issue": issue, "projects": projects, "page_type": "Edit", "page_value": issue.title}, context_instance=RequestContext(request))


@login_required
def history(request, issue_id):
    try:
        issue = Issue.objects.get(pk=issue_id)
        try:
            issue_status_updates = IssueStatusUpdate.objects.filter(issue=issue)
        except Exception, e:
            print e
        try:
            issue_field_updates = IssueFieldUpdate.objects.filter(issue=issue)
        except Exception, e:
            print e
        try:
            historical_issues = IssueHistorical.objects.filter(issue=issue)

            historical_issues_json = []
            for historical_issue in historical_issues:
                historical_issue_dict = model_to_dict(historical_issue)
                historical_issue_dict['modified'] = historical_issue.modified
                historical_issue_dict['projected_start'] = str(historical_issue_dict['projected_start'])
                historical_issue_dict['projected_end'] = str(historical_issue_dict['projected_end'])
                historical_issue_dict['actual_start'] = str(historical_issue_dict['actual_start'])
                historical_issue_dict['actual_end'] = str(historical_issue_dict['actual_end'])
                historical_issue_dict['due_date'] = str(historical_issue_dict['due_date'])
                historical_issue_dict['date_reported'] = str(historical_issue_dict['date_reported'])
                historical_issues_json.append(historical_issue_dict)
        except Exception, e:
            print e
    except Exception, e:
        print e

    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    try:
        users = User.objects.all()
    except Exception, e:
        print "Unable to get user list"
        print e

    form = IssueFullForm(instance=issue)
    page_type = "Issue " + str(issue.id) + ':' + str(issue.summary)

    return render_to_response("issues/issue_history.html", {"issue": issue, "issue_status_updates": issue_status_updates, "issue_field_updates": issue_field_updates, "historical_issues": historical_issues_json, "form": form, "users": users, "projects": projects, "page_type": page_type, "page_value": "History"}, context_instance=RequestContext(request))

@login_required
def issue_search_simple(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    if request.method == "GET":
        return render_to_response("issues/issue_adv_search.html", {"projects": projects},context_instance=RequestContext(request))

    search = request.POST['searchText']
    print search

    q = Issue.objects.filter(Q(summary__contains=search) | Q(description__contains=search))
    return render_to_response("issues/issue_search_results.html", {'results': q, "projects": projects}, context_instance=RequestContext(request))


@login_required
def issue_search_advanced(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    if request.method == "GET":
        return render_to_response("issues/issue_adv_search.html", {'form': AdvSearchForm(), "projects": projects}, context_instance=RequestContext(request))
    form = AdvSearchForm(request.POST)
    if not form.is_valid():
        raise Exception("Invalid adv search form values")
        return redirect('issues.views.issue_advanced_search')
    sq_string = pickle.dumps(form)
    m = hashlib.new('ripemd160')
    m.update(sq_string)
    hash_string =  m.hexdigest()
    try:
        search_hash = AdvancedSearchHash.objects.get(search_hash=hash_string)
        return redirect('issues.views.loadSearchResults', hash_string)
    except Exception, e:
        print "Search Query not in database: Creating new hash"
    try:
        search_hash = AdvancedSearchHash()
        search_hash.search_hash = hash_string
        search_hash.query = sq_string
        search_hash.save()
        return redirect('issues.views.loadSearchResults', search_hash.search_hash)
    except Exception, e:
        print "Search Hash could not be created"
    return render_to_response("issues/issue_adv_search.html", {'form': AdvSearchForm(), "projects": projects}, context_instance=RequestContext(request))


def returnQuery(field_name, field_value):
    if field_name == 'project':
        return Issue.objects.filter(project=field_value), field_value.name
    elif field_name == 'meta_issues':
        return Issue.objects.filter(meta_issues=field_value), field_value.title
    elif field_name == 'assigned_to':
        return Issue.objects.filter(assigned_to=field_value.user), field_value.user.username
    elif field_name == 'created_by':
        return Issue.objects.filter(created_by=field_value.user), field_value.user.username
    elif field_name == 'issue_type':
        return Issue.objects.filter(issue_type=field_value), field_value
    elif field_name == 'status':
        return Issue.objects.filter(status=field_value), field_value
    elif field_name == 'title':
        return Issue.objects.filter(Q(title__contains=field_value)), field_value
    elif field_name == 'summary':
        return Issue.objects.filter(Q(summary__contains=field_value)), field_value
    elif field_name == 'description':
        return Issue.objects.filter(Q(description__contains=field_value)), field_value
    elif field_name == 'os':
        return Issue.objects.filter(Q(os__contains=field_value)), field_value
    elif field_name == 'os_version':
        return Issue.objects.filter(Q(os_version__contains=field_value)), field_value
    elif field_name == 'browser':
        return Issue.objects.filter(Q(browser__contains=field_value)), field_value
    elif field_name == 'browser_version':
        return Issue.objects.filter(Q(browser_version__contains=field_value)), field_value
    elif field_name == 'criticality':
        return Issue.objects.filter(criticality=field_value), field_value
    elif field_name == 'priority':
        return Issue.objects.filter(priority=field_value), field_value
    elif field_name == 'fixability':
        return Issue.objects.filter(fixability=field_value), field_value
    return [],""


query_fields = {'project': 'Projects', 'meta_issues': 'Meta Issues', 'assigned_to': 'Assigned To', 'created_by': 'Created By', 'issue_type': 'Issue Type',
                'status': 'Status', 'title': 'Title', 'summary': 'Summary', 'description': 'Description', 'os': 'OS', 'os_version': 'OS Version', 'browser': 'Browser',
                'browser_version': 'Browser Version', 'criticality': 'Criticality', 'priority': 'Priority', 'fixability': 'Fixability'}


def returnDateQuery(start, end, field):
    # function called by loadSearchResults()... returns Issue Queryset based on dates created (or modified)
    start_yr = start.strftime('%Y')
    start_mo = start.strftime('%m')
    start_da = start.strftime('%d')
    date_range_start = str(start_yr) + '-' + str(start_mo) + '-' + str(start_da)
    stop_yr = end.strftime('%Y')
    stop_mo = end.strftime('%m')
    stop_da = end.strftime('%d')
    date_range_end = str(stop_yr) + '-' + str(stop_mo) + '-' + str(stop_da)
    if field == 'created':
        if start <= end:
            return Issue.objects.filter(created__range=[date_range_start, date_range_end])
        else:
            return Issue.objects.filter(created__range=[date_range_end, date_range_start])
    elif field == 'modified':
        if start <= end:
            return Issue.objects.filter(modified__range=[date_range_start, date_range_end])
        else:
            return Issue.objects.filter(modified__range=[date_range_end, date_range_start])
    return []


def returnDayQuery(date, field):
    # returns Issue Queryset created (or modified) on a specific date
    yr = date.strftime('%Y')
    mo = date.strftime('%m')
    da = date.strftime('%d')
    date_range = str(yr) + '-' + str(mo) + '-' + str(da)
    if field == 'created':
        return Issue.objects.filter(created__range=[date_range, date_range])
    elif field == 'modified':
        return Issue.objects.filter(modified__range=[date_range, date_range])
    return []


def loadSearchResults(request, search_hash_id):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        # load hashed search query (pickled form is stored in AdvancedSearchHash object)
        search_hash = AdvancedSearchHash.objects.get(search_hash=search_hash_id)
        search_hash.modified = date.today()
        search_hash.save()
        query = pickle.loads(search_hash.query)
        q = []
        # params is used to pass a list of fields + values (that were used to make the query)
        # params is passed as a JSON object to be displayed on the page
        params = {}
        return_params = {}
        by_created = False
        by_modified = False
        for field in query.cleaned_data.keys():
            temp = []
            if field == 'created_start' or field == 'created_stop':
                # Search by date created requires special handling
                if not by_created:
                    start = None
                    query_stop = None
                    if query.cleaned_data['created_start'] and query.cleaned_data['created_stop']:
                        start = query.cleaned_data['created_start']
                        query_stop = query.cleaned_data['created_stop']
                        temp.extend(returnDateQuery(start, query_stop, 'created'))
                    elif query.cleaned_data['created_start']:
                        start = query.cleaned_data['created_start']
                        temp.extend(returnDayQuery(start, 'created'))
                    elif query.cleaned_data['created_stop']:
                        start = query.cleaned_data['created_stop']
                        temp.extend(returnDayQuery(start, 'created'))
                    if query.cleaned_data['created_stop']:
                        params['Date Range (Created)'] = [[start.strftime("%b %d %Y") + " - " + query_stop.strftime("%b %d %Y"), 'skip']]
                        return_params['created_stop'] = [[query_stop.strftime("%b %d %Y"), 'skip']]
                        return_params['created_start'] = [[start.strftime("%b %d %Y"), 'skip']]
                    elif start:
                        params['Date (Created)'] = [[start.strftime("%b %d %Y"), 'skip']]
                        return_params['created_start'] = [[start.strftime("%b %d %Y"), 'skip']]
                    if temp:
                        if q:
                            q = list(set(q) & set(temp))
                        else:
                            q.extend(temp)
                    by_created = True
            elif field == 'modified_start' or field == 'modified_stop':
                # Search by date modified requires special handling
                if not by_modified:
                    start = None
                    query_stop = None
                    if query.cleaned_data['modified_start'] and query.cleaned_data['modified_stop']:
                        start = query.cleaned_data['modified_start']
                        query_stop = query.cleaned_data['modified_stop']
                        temp.extend(returnDateQuery(start, query_stop, 'modified'))
                    elif query.cleaned_data['modified_start']:
                        start = query.cleaned_data['created_start']
                        temp.extend(returnDayQuery(start, 'modified'))
                    elif query.cleaned_data['modified_stop']:
                        start = query.cleaned_data['modified_stop']
                        temp.extend(returnDayQuery(start, 'modified'))
                    if query.cleaned_data['modified_stop']:
                        params['Date Range (Modified)'] = [[start.strftime("%b %d %Y") + " - " + query_stop.strftime("%b %d %Y"), 'skip']]
                        return_params['modified_start'] = [[start.strftime("%b %d %Y"), 'skip']]
                        return_params['modified_stop'] = [[query_stop.strftime("%b %d %Y"), 'skip']]
                    elif start:
                        params['Date (Modified)'] = [[start.strftime("%b %d %Y"), 'skip']]
                        return_params['modified_start'] = [[start.strftime("%b %d %Y"), 'skip']]
                    if temp:
                        if q:
                            q = list(set(q) & set(temp))
                        else:
                            q.extend(temp)
                    by_modified = True
            elif query.cleaned_data[field]:
                # All non-Date related fields are handled by this code
                params[query_fields[field]] = []
                return_params[field] = []
                completed_values = []
                for value in query.cleaned_data[field]:
                    if value not in completed_values:
                        temp2, param_value = returnQuery(field, value)
                        params[query_fields[field]].append([param_value, field])
                        return_params[field].append(value.id)
                        completed_values.append(value)
                        if temp:
                            temp = temp | temp2
                        else:
                            temp = temp2
                if q:
                    q = list(set(q) & set(temp))
                else:
                    q.extend(temp)
    except Exception, e:
        print e
        return redirect('issues.views.issue_search_advanced')
    return render_to_response("issues/adv_search_results.html", {'projects': projects,
                                                                 'issues': q,
                                                                 'query': json.dumps(params),
                                                                 'return_query': json.dumps(return_params),
                                                                 'form': AdvSearchForm(),}, context_instance=RequestContext(request))

'''
@login_required
def issue_search_advanced(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    if request.method == "GET":
        return render_to_response("issues/issue_adv_search.html", {'form': AdvSearchForm(), "projects": projects}, context_instance=RequestContext(request))

    print request.POST

    form = AdvSearchForm(request.POST)
    if not form.is_valid():
        raise Exception("Invalid adv search form values")

    query = None

    for field in form.cleaned_data.keys():
        # print field
        # print form.cleaned_data[field]
        qr = None
        if not form.cleaned_data[field]:
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
    if query:
        print query
        results = Issue.objects.filter(query)
    else:
        print query
        return render_to_response("issues/issue_adv_search.html", {'form': AdvSearchForm(), "projects": projects}, context_instance=RequestContext(request))
    return render_to_response("issues/issue_search_results.html", {'results': results, "projects": projects}, context_instance=RequestContext(request))
'''

@login_required
def edit_comment(request):
    to_json = {'success': True}

    try:
        comment = IssueComment.objects.get(pk=request.POST['comment_id'])
        comment.description = request.POST['comment']
        comment.save(request.user)
    except Exception, e:
        print e
        to_json['success'] = False

    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
@permission_required("issues.add_issuecomment", raise_exception=True)
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
        comments = IssueComment.objects.filter(issue=issue).order_by('-created')  # this isn't used; why are we making an extra call?
    except Exception, e:
        print "Error getting comments"
        raise e

    comment = IssueComment()

    if request.method == 'POST':
        for k in request.POST:
            print k
            print request.POST[k]
        try:
            #
            form = CommentForm(request.POST, instance=comment)
            #
            if form.is_valid():
                try:
                    comment = form.save(request.user)  # save the modelform's model!
                    prepMail.delay(issue, "comment", comment.description)
                except Exception, e:
                    print "Error saving form"
                    print e
                    print form.errors
            else:
                print "comment form not valid"
                # print form
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
    projects = Project.objects.all()
    q = Issue.objects.filter(Q(assigned_to__isnull=True) & (Q(status="active") | Q(status="retest") | Q(status="unverified") | Q(status__isnull=True))).order_by('created')
    return render_to_response('issues/issue_unassigned.html', {'issues': q, 'projects': projects}, context_instance=RequestContext(request))


def testView(request):
    form = TestForm()
    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
    return render_to_response("issues/test_form.html", {'form': form, "projects": projects}, context_instance=RequestContext(request))

'''
def set_issue_start_and_end_dates(request):
    success_or_fail = "Success!"
    try:
        issues = Issue.objects.all()

        for issue in issues:
            if not issue.projected_start:
                issue.projected_start = issue.created
            if not issue.projected_end:
                if issue.modified:
                    issue.projected_end = issue.modified
                else:
                    issue.projected_end = datetime.date.today()
            if not issue.actual_start:
                issue.actual_start = issue.created
            if not issue.actual_end:
                if issue.modified:
                    issue.actual_end = issue.modified
            issue.save()
    except Exception, e:
        print e
        success_or_fail = "Fail: " + str(e)

    return render_to_response("issues/set_issue_start_and_end_dates.html", {"success_or_fail": success_or_fail}, context_instance=RequestContext(request))
'''

@login_required
def trackIssues(request, tracker_hash=0):
    if not tracker_hash == 0:
        try:
            tracker = TrackerHash.objects.get(query_hash=tracker_hash)
            query_dict = convertStringToDict(tracker.query_string)
        except Exception, e:
            print e
    elif request.method == "POST":
        query_dict = request.POST
    max_count = int(query_dict['filter_count'][0])
    q = []
    issues = {}
    return_queries = 0
    return_query = []
    for x in range(max_count + 1):
        if str(x) in query_dict:
            try:
                if tracker_hash == 0:
                    command = query_dict.getlist(str(x))
                else:
                    command = query_dict[str(x)]
                if command[0] in issues:
                    issues[command[0]] = list(set(issues[command[0]]) | set(evaluateCommand(command[0], command[1], command[2])))
                else:
                    issues[command[0]] = evaluateCommand(command[0], command[1], command[2])
                return_query.append(command)
                return_queries = return_queries + 1
            except:
                pass
    for k in issues:
        if q:
            q = list(set(q) & set(issues[k]))
        else:
            q = issues[k]
    if tracker_hash == 0:
        temp_list = []
        for issue in q:
            if issue.meta_issues:
                meta_issue_id = issue.meta_issues.id
                meta_issue_name = issue.meta_issues.title
            else:
                meta_issue_id, meta_issue_name = "None", "None"
            if issue.sprint:
                sprint_id = issue.sprint.id
                sprint_name = issue.sprint.name
            else:
                sprint_id, sprint_name = "None", "None"
            if issue.assigned_to:
                assigned_to_id = issue.assigned_to.id
                assigned_to_username = issue.assigned_to.username
            else:
                assigned_to_id, assigned_to_username = "None", "None"
            temp = {'id': issue.id,
                    'summary': issue.summary,
                    'assigned_to_id': assigned_to_id,
                    'assigned_to_username': assigned_to_username,
                    'criticality': issue.criticality,
                    'status': issue.status,
                    'project_id': issue.project.id,
                    'project_name': issue.project.name,
                    'meta_issue_id': meta_issue_id,
                    'meta_issue_name': meta_issue_name,
                    'sprint_id': sprint_id,
                    'sprint_name': sprint_name,
                    'created': datetime.strftime(issue.created, "%D %I:%M %p"),
                    'modified': datetime.strftime(issue.modified, "%D %I:%M %p"),}
            temp_list.append(temp)
        to_json = {}
        to_json["hist"] = return_query
        to_json["total_filters"] = return_queries
        to_json["issues"] = temp_list
        return HttpResponse(json.dumps(to_json))
    else:
        try:
            saved_queries = TrackerHash.objects.filter(user=request.user)
        except Exception, e:
            print e
        return render_to_response("issues/overview.html", {'user': request.user, 
                                                           'issues': q, 
                                                           'total_filters': return_queries,
                                                           'saved_queries': saved_queries,
                                                           'applied_filters': json.dumps(return_query), 
                                                           'json_query': json.dumps(issueTrackerQueryMaker())}, context_instance=RequestContext(request))


def issueTrackerQueryMaker():
    to_json = {"options": ["Project", "Assigned User", "Meta Issue", "Status", "Sprint"]}
    try:
        projects = Project.objects.all()
        to_json["Project"] = []
        for project in projects:
            to_json["Project"].append(project.name)
    except Exception, e:
        print e
    try:
        users = Account.objects.filter(assignable=True)
        to_json["Assigned User"] = []
        for user in users:
            to_json["Assigned User"].append(user.user.username)
    except Exception, e:
        print e
    try:
        meta_issues = MetaIssue.objects.all()
        to_json["Meta Issue"] = []
        for meta in meta_issues:
            to_json["Meta Issue"].append(meta.title)
    except Exception, e:
        print e
    try:
        sprints = Sprint.objects.all()
        to_json["Sprint"] = []
        for sprint in sprints:
            to_json["Sprint"].append(sprint.name)
    except Exception, e:
        print e
    return to_json


@login_required
def overview(request):
    
    try:
        issues = Issue.objects.order_by('-created')
    except Exception, e:
        print e
        issues = []
    
    return render_to_response("issues/overview.html", {"issues": issues}, context_instance=RequestContext(request))


@login_required
def assign_to_user(request, user_id, issue_id):
    to_json = {'success': True, 'is_subscribed': False, 'error': False}
    try:
        issue = Issue.objects.get(pk=issue_id)
    except Exception, e:
        to_json['success'] = False
        to_json['error'] = str(e)
    if user_id == 0:
        issue.assigned_to = None
        issue.save()
        return HttpResponse(json.dumps(to_json), mimetype="application/json")
    try:
        user = User.objects.get(pk=user_id)
    except Exception, e:
        to_json['success'] = False
        to_json['error'] = str(e)
    try:
        issue.assigned_to = user
        issue.save()
        to_json["data"] = model_to_dict(issue)
        to_json["data"]["assigned_to"] = user.username
    except Exception, e:
        to_json['success'] = False
        to_json['error'] = str(e)
    return HttpResponse(json.dumps(to_json), mimetype="application/json")


@login_required
def tempTrack(request):
    try:
        saved_queries = TrackerHash.objects.filter(user=request.user)
    except Exception, e:
        print e
    if issues:
        q = issues
    else:
        q = Issue.objects.all()
    return_queries = 0
    return_query = {}
    return render_to_response("issues/overview.html", {'user': request.user, 
                                                       'issues': q, 
                                                       'total_filters': return_queries,
                                                       'saved_queries': saved_queries,
                                                       'applied_filters': json.dumps(return_query), 
                                                       'json_query': json.dumps(issueTrackerQueryMaker())}, context_instance=RequestContext(request))


def evaluateCommand(field, op, value):
    if value is None:
        return []
    keys = {"Project": "project__name", "Assigned User": "assigned_to__username", "Meta Issue": "meta_issues__title", "Status": "status", "Sprint": "sprint__name"}
    kwargs = {keys[field]: value}
    if field == "Status" and value == "None":
        return Issue.objects.filter(status__isnull=True)
    if op == "is":
        return Issue.objects.filter(**kwargs)
    else:
        return Issue.objects.exclude(**kwargs)


def convertDictToString(dictionary):
    dict_string = "total_filters=%s&" % dictionary["total_filters"]
    count = 0
    for command in dictionary["hist"]:
        temp = "%s=" % count
        for article in command:
            temp = temp + "%s," % str(article)
        dict_string = dict_string + "%s&" % temp[:-1]
        count = count + 1
    return dict_string[:-1]


def convertStringToDict(dict_string):
    dict_array = dict_string.split("&")
    total_count = []
    total_count.append(unicode(dict_array[0].split("=")[1]))
    my_dict = {"filter_count": total_count}
    for x in range(0,int(dict_array[0].split("=")[1])):
        my_dict[str(x)] = dict_array[x+1].split("=")[1].split(",")
    return my_dict


def saveFilterSet(request):
    if request.method == "POST":
        max_count = int(request.POST.getlist('filter_count')[0])
        return_queries = 0
        return_query = []
        for x in range(max_count + 1):
            if str(x) in request.POST:
                try:
                    command = request.POST.getlist(str(x))
                    return_query.append(command)
                    return_queries = return_queries + 1
                except:
                    pass
        to_json = {}
        to_json["hist"] = return_query
        to_json["total_filters"] = return_queries
        query_string = convertDictToString(to_json) + "&user=" + str(request.user.id)
        m = hashlib.new('ripemd160')
        m.update(query_string)
        hash_string =  m.hexdigest()
        try:
            query_hash = TrackerHash(query_string=query_string, query_hash=hash_string, user=request.user, name=request.GET.get("name"))
            query_hash.save()
        except Exception, e:
            print e
    return redirect('issues.views.tempTrack')