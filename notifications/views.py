# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from projects.models import Project
from notifications.models import Notification, NotificationRecipient
from notifications.forms import NotificationForm
from django.forms.models import inlineformset_factory

import json


@login_required
def notification_form(request):

    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
        projects = []

    NotificationRecipientsFormset = inlineformset_factory(Notification, NotificationRecipient, can_delete=False, extra=1)
    notification = Notification()

    if request.method == 'POST':
        notification_form = NotificationForm(request.POST, instance=notification)
        formset = NotificationRecipientsFormset(request.POST, instance=notification)
        if notification_form.is_valid() and formset.is_valid():
            n = notification_form.save()
            formset.save()
            print 'saving form'
            return redirect('dashboard.views.home')
        else:
            print notification_form.errors
            print formset.errors
    else:
        formset = NotificationRecipientsFormset(instance=notification)

    notification_form = NotificationForm(instance=notification, auto_id=False)

    return render_to_response("notifications/notification_form.html", {'formset': formset, "notification_form": notification_form, "projects": projects, "page_type": "Notification", "page_value": "New"}, context_instance=RequestContext(request))
