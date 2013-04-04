# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import DailyReportForm
from models import UserDailyReport


def daily_report_form(request):
    if request.method == 'POST':
        report = UserDailyReport()
        form = DailyReportForm(request.POST, instance=report)
        if form.is_valid():
            try:
                report = form.save()
            except Exception, e:
                print e
            if report.id:
                return redirect('daily_reports.views.daily_report_overview', report.id, permanent=True)
            else:
                return render_to_response('daily_reports/daily_report_form.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = DailyReportForm()
        print form
    return render_to_response("daily_reports/daily_report_form.html", {'form': form}, context_instance=RequestContext(request))


def daily_report_overview(request, report_id):
    try:
        report = UserDailyReport.objects.get(pk=report_id)
    except:
        print "Somebody messed up the report overview"
    return render_to_response("daily_reports/daily_report_overview.html", {'report': report}, context_instance=RequestContext(request))
