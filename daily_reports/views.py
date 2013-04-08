# Create your views here.
from datetime import date
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import ReportForm
from models import UserDailyReport


@login_required
def edit_report_today(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                q = UserDailyReport.objects.filter(user=request.user.id, date=form.cleaned_data['date'])
                report = q[0] if q else UserDailyReport(user=request.user.id, date=form.cleaned_data['date'])
                report.description = form.cleaned_data['personalReport']
                report.save()
                return redirect('daily_reports.views.edit_report_today', permanent=True)
            except Exception, e:
                print e
                return render_to_response('daily_reports/daily_report_form.html', {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('daily_reports/daily_report_form.html', {'form': form}, context_instance=RequestContext(request))

    else:
        q = None
        try:
            q = UserDailyReport.objects.filter(user=request.user.id, date=date.today())
        except Exception, e:
            print "Exception: " + str(e)
            raise e
        if q:
            form = ReportForm(initial={"date": date.today(), "personalReport": q[0].description})
        else:
            form = ReportForm(initial={"date": date.today()})
            print "no report"
        # print form
    return render_to_response("daily_reports/daily_report_form.html", {'form': form}, context_instance=RequestContext(request))


@login_required
def edit_report(request, year, month, day):
    try:
        d = date(int(year), int(month), int(day))
    except:
        year = "0"

    if (int(year) < 2013 or int(year) > date.today().year + 1):
        return redirect('daily_reports.views.edit_report_today')

    print d
    q = None
    try:
        q = UserDailyReport.objects.filter(user=request.user.id, date=d)
    except Exception, e:
        print "Exception: " + str(e)
        raise e
    if q:
        form = ReportForm(initial={"date": d, "personalReport": q[0].description})
    else:
        form = ReportForm(initial={"date": d})
        print "no report"
    # print form
    return render_to_response("daily_reports/daily_report_form.html", {'form': form}, context_instance=RequestContext(request))
