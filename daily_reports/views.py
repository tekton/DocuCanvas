# Create your views here.
from datetime import date
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import ReportForm
from models import *


@login_required
def edit_report(request, year=0, month=0, day=0):
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
                return render_to_response('daily_reports/daily_report_form.html', {'form': context_instance}, form=RequestContext(request))
        else:
            return render_to_response('daily_reports/daily_report_form.html', {'form': form, 'global': False}, context_instance=RequestContext(request))

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
        if q:
            form = ReportForm(initial={"date": d, "personalReport": q[0].description})
        else:
            form = ReportForm(initial={"date": d})
        return render_to_response("daily_reports/daily_report_form.html", {'form': form, 'global': False}, context_instance=RequestContext(request))


def edit_global_report(request, year=0, month=0, day=0):
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
                return render_to_response('daily_reports/daily_report_form.html', {'form': form, 'global': True}, context_instance=RequestContext(request))
        else:
            return render_to_response('daily_reports/daily_report_form.html', {'form': form, 'global': True}, context_instance=RequestContext(request))

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
        return render_to_response("daily_reports/daily_report_form.html", {'form': form, 'global': True}, context_instance=RequestContext(request))


def view_reports(request, year=0, month=0, day=0):
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
        return render_to_response("daily_reports/daily_report_overview.html", {'globalReport': qg[0], 'reports': q, 'date': d}, context_instance=RequestContext(request))
    else:
        return render_to_response("daily_reports/daily_report_overview.html", {'globalReports': None, 'reports': q, 'date': d}, context_instance=RequestContext(request))
