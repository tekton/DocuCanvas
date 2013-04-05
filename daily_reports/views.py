# Create your views here.
from datetime import date
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import DailyReportForm
from models import UserDailyReport


@login_required
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
                return redirect('daily_reports.views.daily_report_form', permanent=True)
            else:
                return render_to_response('daily_reports/daily_report_form.html', {'form': form}, context_instance=RequestContext(request))
    else:
        try:
            report = UserDailyReport.objects.get(user_id__exact=request.user.id, date__exact=date.today())
            form = DailyReportForm(instance=report)
        except:
            report = UserDailyReport()
            form = DailyReportForm({"user": request.user.id, "date": date.today()}, instance=report)
        # print form
    return render_to_response("daily_reports/daily_report_form.html", {'form': form}, context_instance=RequestContext(request))

