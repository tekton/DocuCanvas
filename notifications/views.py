# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from projects.models import Project
from notifications.models import Notification, NotificationRecipient
from notifications.forms import NotificationForm

import json


@login_required
def notification_form(request):
    if request.method == 'POST':
        notification = Notification()
        try:
            form = NotificationForm(request.POST, instance=notification)
            if form.is_valid():

                try:
                    notification = form.save()
                except Exception, e:
                    print 'unable to save notification'
                    print e
                if notification.id:
                    return redirect('dashboard.views.home')
                else:
                    return render_to_response("notifications/notification_form.html", {'form': form}, context_instance=RequestContext(request))
        except Exception, e:
            print "Error validating notification fields"
            print e
    else:
        form = NotificationForm()
        try:
            projects = Project.objects.all()
        except:
            print 'Unable to grab all projects'

    return render_to_response("notifications/notification_form.html", {'form': form, "projects": projects, "page_type": "Notification", "page_value": "New"}, context_instance=RequestContext(request))
