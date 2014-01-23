from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime as timedate

from forms import ReportForm, GroupForm, DailyReportForm
from projects.models import Project
from newsfeed.models import NewsFeedItem
from models import UserDailyReport, DailyReport, ReportGroup, GroupMember

import datetime


@login_required
def edit_report(request, year=None, month=None, day=None):
    projects = Project.objects.all()
    if year is None:
        report_date = date.today()
        # redirect to view with that for simplicity sake and consistency sake
        return redirect('daily_reports.views.edit_report', report_date.strftime("%Y"),
                                                           report_date.strftime("%m"),
                                                           report_date.strftime("%d"))
    else:
        report_date = date(int(year), int(month), int(day)).strftime("%Y-%m-%d")
    print report_date
    
    form = DailyReportForm(initial={'date': report_date, 'user': request.user})

    if request.method == 'POST':
        try:
            report = UserDailyReport.objects.get(user=request.user, date=report_date)
        except:
            # print "Unable to find report; assuming new entry not an edit functionality"  # debug statement as it were
            report = UserDailyReport()
            report.user = request.user  # hacky, but will work for now...
        try:
            form = DailyReportForm(request.POST, instance=report)
            form.user = request.user  # sometimes this wasn't applying above, here as a security measure for now- use admin to edit someone elses for now
            form.save()
        except Exception as e:
            print "Unable to save form due to :: {}".format(str(e))
    else:
        try:
            report = UserDailyReport.objects.get(user=request.user.id, date=report_date)
            form = DailyReportForm(instance=report)
        except:
            print "unable to find daily report"

    return render_to_response('daily_reports/daily_report_form.html',
                              {'form': form,
                               'projects': projects,
                               'report_date': report_date,
                               'year': year,'month': month,'day': day,},
                              context_instance=RequestContext(request)
                             )


@login_required
def edit_global_report(request, month=0, day=0, year=0):
    projects = Project.objects.all()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                q = DailyReport.objects.filter(date=form.cleaned_data['date'])
                report = q[0] if q else DailyReport(date=form.cleaned_data['date'])
                report.description = form.cleaned_data['personalReport']
                report.save()
                return redirect('daily_reports.views.edit_global_report')
            except Exception as e:
                print e
                return render_to_response('daily_reports/daily_report_form.html', {'form': form, 'global': True, "projects": projects}, context_instance=RequestContext(request))
        else:
            return render_to_response('daily_reports/daily_report_form.html', {'form': form, 'global': True, "projects": projects}, context_instance=RequestContext(request))

    else:
        d = date.today()
        if (year != 0):
            try:
                d = date(int(year), int(month), int(day))
            except:
                return redirect('daily_reports.views.edit_global_report')

            if (d.year < 2013 or d.year > date.today().year + 1):
                return redirect('daily_reports.views.edit_global_report')

        q = None
        try:
            q = DailyReport.objects.filter(date=d)
        except Exception as e:
            print "Exception: " + str(e)
            raise e
        if q:
            form = ReportForm(initial={"date": d, "personalReport": q[0].description})
        else:
            form = ReportForm(initial={"date": d})
        return render_to_response("daily_reports/daily_report_form.html", {'form': form, 'global': True, "projects": projects}, context_instance=RequestContext(request))


@login_required
def view_reports(request, month=0, day=0, year=0):
    projects = Project.objects.all()
    d = date.today()
    if (year != 0):
        try:
            d = date(int(year), int(month), int(day))
        except:
            return redirect("daily_reports.views.view_reports")

    try:
        q = UserDailyReport.objects.filter(date=d)
        qg = DailyReport.objects.filter(date=d)
    except Exception as e:
        print "Exception: " + str(e)
        raise e

    if qg:
        return render_to_response("daily_reports/daily_report_overview.html", {'globalReport': qg[0], 'reports': q, 'date': d, "projects": projects}, context_instance=RequestContext(request))
    else:
        return render_to_response("daily_reports/daily_report_overview.html", {'globalReports': None, 'reports': q, 'date': d, "projects": projects}, context_instance=RequestContext(request))


def mail_report():
    projects = Project.objects.all()
    d = date.today()
    try:
        q = UserDailyReport.objects.filter(date=d)
        qg = DailyReport.objects.filter(date=d)
    except Exception as e:
        print "Exception: " + str(e)
        raise e
    return render_to_response("daily_reports/daily_report_overview.html", {'globalReport': qg[0], 'reports': q, 'date': d, "projects": projects}, context_instance=RequestContext(request))

    email_subject = "Daily Report " + str(d)
    email_sender = "test@replace_me.com"
    try:
        email_recipients = ["generic@brand.net"]
        htmly = get_template('daily_reports/daily_report_overview.html')

        text_content = 'Todays daily report'
        d = Context({'globalReport': qg[0], 'reports': q, 'date': d})

        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(email_subject, text_content, email_sender, email_recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except:
        return False


@login_required
def index(request):
    projects = Project.objects.all()
    reports = UserDailyReport.objects.filter(user=request.user).order_by('-date')[:5]
    # check if there's a report for today...
    now = datetime.datetime.now()
    try:
        today_report = UserDailyReport.objects.get(user=request.user, date=now.strftime("%Y-%m-%d"))
        today = False
    except Exception as e:
        print "Unable to get todays report"
        print e
        today = True
    return render_to_response("daily_reports/report_index.html", {"reports": reports,
                                                                  "projects": projects,
                                                                  "today": today,
                                                                  "page_type": "Report"}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def setup_report_group(request):
    projects = Project.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        try:
            group = ReportGroup()
            form = GroupForm(request.POST, instance=group)
            members = request.POST.getlist('users')
            if form.is_valid():
                group = form.save()
                for member in members:
                    temp = User.objects.get(username=member)
                    new_member = GroupMember(group=group, user=temp)
                    new_member.save()
                return redirect('daily_reports.views.request_report_summary')
        except Exception as e:
            print "Exception: " + str(e)
    else:
        form = GroupForm()
    return render_to_response('daily_reports/report_group_form.html', {'users': users, 'projects': projects, 'form': form}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def edit_group(request, group_id):
    projects = Project.objects.all()
    print request.POST
    try:
        group = ReportGroup.objects.get(pk=group_id)
    except Exception as e:
        print "Exception: " + str(e)
    try:
        members = GroupMember.objects.filter(group=group)
    except Exception as e:
        print "Exception: " + str(e)
    try:
        users = User.objects.all()
        user_list = []
        for user in users:
            keep = True
            for member in members:
                if member.user == user:
                    keep = False
            if keep:
                user_list.append(user)

    except Exception as e:
        print "Exception: " + str(e)
    if request.method == 'POST':
        try:
            form = GroupForm(request.POST, instance=group)
            added_members = request.POST.getlist('new_members')
            removed_members = request.POST.getlist('del_members')
            if form.is_valid():
                group = form.save()
                for member in added_members:
                    temp = User.objects.get(pk=member)
                    new_member = GroupMember(group=group, user=temp)
                    new_member.save()
                for member in removed_members:
                    temp = User.objects.get(pk=member)
                    old_member = GroupMember.objects.get(user=temp, group=group)
                    old_member.delete()
                return redirect('daily_reports.views.request_report_summary')
        except Exception as e:
            print e
    else:
        form = GroupForm(instance=group)
    return render_to_response('daily_reports/edit_report_group.html', {'members': members, 'users': user_list, 'form': form, 'projects': projects, 'group': group}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def request_report_summary(request):
    projects = Project.objects.all()
    groups = ReportGroup.objects.all()
    return render_to_response('daily_reports/group_report.html', {'projects': projects, 'groups': groups}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def report_summary(request, year_start, month_start, day_start, year_end,  month_end, day_end, group_id):
    projects = Project.objects.all()

    date_range_start = str(year_start) + '-' + str(month_start) + '-' + str(day_start)
    date_range_end = str(year_end) + '-' + str(month_end) + '-' + str(day_end)

    start = datetime.date(year=int(year_start), month=int(month_start), day=int(day_start))
    end = datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))

    dates = []
    for date in daterange(start, end):
        dates.append(date)

    group = ReportGroup.objects.get(pk=group_id)
    users = GroupMember.objects.filter(group=group)

    reports = UserDailyReport.objects.filter(date__range=[date_range_start, date_range_end]).order_by('date')

    return render_to_response('daily_reports/report_summary.html', {'users': users, 'reports': reports, 'projects': projects, 'dates': dates}, context_instance=RequestContext(request))


def daterange(start_date, end_date):
    if start_date <= end_date:
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)
    else:
        for n in range((start_date - end_date).days + 1):
            yield start_date - datetime.timedelta(n)


@login_required
def reportRedirect(request):
    try:
        d = str(request.GET.get('date',False))
        temp = ''
        count = 0
        searching = True
        for char in d:
            if searching and count > 2:
                if char == " ":
                    searching = False
                    temp += char
            elif char != "." and char != ",":
                temp += char
            count += 1
        date_object = timedate.strptime(temp, '%b %d %Y')
        day = date_object.strftime('%d')
        month = date_object.strftime('%m')
        year = date_object.strftime('%Y')
    except:
        d = date.today()
        day = d.strftime('%d')
        month = d.strftime('%m')
        year = d.strftime('%Y')
    return redirect('daily_reports.views.view_reports', month, day, year)


@user_passes_test(lambda u: u.is_superuser)
def view_reports_wip(request, year_start, month_start, day_start, year_end,  month_end, day_end):
    projects = Project.objects.all()
    date_range_start = str(year_start) + '-' + str(month_start) + '-' + str(day_start)
    date_range_end = str(year_end) + '-' + str(month_end) + '-' + str(day_end)
    print date_range_start
    users = User.objects.all()

    reports = UserDailyReport.objects.filter(date__range=[date_range_start, date_range_end]).order_by('date')
    newsfeeditems = NewsFeedItem.objects.filter(timestamp__range=[date_range_start, date_range_end]).order_by('user','project','field_change')

    return render_to_response('daily_reports/reports_overview_wip.html', {'users': users, 'newsfeeditems':newsfeeditems, 'reports': reports, 'projects':projects}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def report_selection(request):
    projects = Project.objects.all()
    return render_to_response('daily_reports/report_selection.html',{'projects':projects}, context_instance=RequestContext(request))
