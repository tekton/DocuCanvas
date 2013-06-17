# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from projects.models import Project
from notifications.models import Notification, NotificationRecipient
from notifications.forms import NotificationForm, NotificationRecipientForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

import json


@login_required
def notification_form(request):

    if request.user.is_superuser:
        users_list = []
        users_dict = {}
        num_users = 0

        try:
            projects = Project.objects.all()
        except Exception, e:
            print e
            projects = []

        try:
            users = User.objects.all()
            for user in users:
                user_dict = model_to_dict(user)
                users_dict[user_dict['id']] = user_dict['username']
                num_users += 1
        except Exception, e:
            print e
            users = []

        NotificationRecipientsFormset = inlineformset_factory(Notification, NotificationRecipient, can_delete=False, extra=1)
        notification = Notification()
        notification_recipient = NotificationRecipient()

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
            formset = NotificationRecipientsFormset(instance=notification, initial=[
            {'read': False}])

        notification_form = NotificationForm(instance=notification, auto_id=False)
    else:
        return redirect('dashboard.views.home')

    return render_to_response("notifications/notification_form.html", {'formset': formset, "notification_form": notification_form, "users": json.dumps(users_dict), "num_users": num_users, "projects": projects, "page_type": "Notification", "page_value": "New"}, context_instance=RequestContext(request))


@login_required
def notifications(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
        projects = []

    try:
        notifications = NotificationRecipient.objects.select_related().filter(user=request.user,read=True)
    except Exception, e:
        print e
    return render_to_response("notifications/notifications.html", {"notifications": notifications, "projects": projects, "page_type": "Notification", "page_value": "Past"}, context_instance=RequestContext(request))


@login_required
def mark_as_read(request):
    to_json = {'success': False}

    if request.method == 'POST':
        try:
            notification_recipient = NotificationRecipient.objects.get(pk=request.POST['notification_id'])
            notification_recipient.read = True
            notification_recipient.save()
            to_json['success'] = True
        except Exception, e:
            print e
    return HttpResponse(json.dumps(to_json), mimetype='application/json')
