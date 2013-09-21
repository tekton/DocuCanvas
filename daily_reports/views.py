from datetime import date
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from forms import ReportForm
from projects.models import Project
from newsfeed.models import NewsFeedItem
from models import *

import datetime


@login_required
def edit_report(request, month=0, day=0, year=0):
    projects = Project.objects.all()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                q = UserDailyReport.objects.filter(user=request.user, date=form.cleaned_data['date'])
                report = q[0] if q else UserDailyReport(user=request.user, date=form.cleaned_data['date'])
                report.description = form.cleaned_data['personalReport']
                report.save()
                return redirect('daily_reports.views.edit_report')
            except Exception, e:
                print e
                return render_to_response('daily_reports/daily_report_form.html', {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('daily_reports/daily_report_form.html', {'form': form, 'global': False, "projects": projects}, context_instance=RequestContext(request))

    else:
        d = date.today()
        if (year != 0):
            try:
                d = date(int(year), int(month), int(day))
            except:
                return redirect('daily_reports.views.edit_report')

            if (d.year < 2013 or d.year > date.today().year + 1):
                return redirect('daily_reports.views.edit_report')

        q = None
        try:
            q = UserDailyReport.objects.filter(user=request.user, date=d)
        except Exception, e:
            print "Exception: " + str(e)
            raise e
        dir(q)
        if q:
            form = ReportForm(initial={"date": d, "personalReport": q[0].description})
        else:
            form = ReportForm(initial={"date": d})
        return render_to_response("daily_reports/daily_report_form.html", {'form': form, 'global': False, "projects": projects}, context_instance=RequestContext(request))


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
            except Exception, e:
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
        except Exception, e:
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
    except Exception, e:
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
    except Exception, e:
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


@login_required
def report_summary(request, year_start, month_start, day_start, year_end,  month_end, day_end, group_id):
    projects = Project.objects.all()

    date_range_start = str(year_start) + '-' + str(month_start) + '-' + str(day_start)
    date_range_end = str(year_end) + '-' + str(month_end) + '-' + str(day_end)

    group = ReportGroup.objects.get(pk=group_id)
    users = GroupMember.objects.filter(group=group)

    reports = UserDailyReport.objects.filter(date__range=[date_range_start, date_range_end]).order_by('date')

    count = 0
    for user in users:
        user_reports = reports.filter(user=user.user)
        if user_reports.count() > count:
            benchmark = user_reports

    return render_to_response('daily_reports/report_summary.html', {'users': users, 'reports': reports, 'projects': projects, 'benchmark': benchmark}, context_instance=RequestContext(request))


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
