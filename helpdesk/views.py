from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from helpdesk.forms import HelpForm, HelpFormComplete
from helpdesk.models import HelpRequest


def help_form(request):
	if request.method == 'POST':
		help = HelpRequest()
		helpform = HelpForm(request.POST, request.FILES, instance=help)
		try:
			help = helpform.save()
		except Exception, e:
			print "unable to save help form!"
			print e
		if help.id:
			print "redirecting to view"
			redirect('helpdesk.views.get_help', help.id)
		else:
			print "something went wrong"
			print help
	else:
		helpform = HelpForm()
	return render_to_response('helpdesk/help_form.html', {'form': helpform}, context_instance=RequestContext(request))


def get_help(request, help_id):
	try:
		help = HelpRequest.objects.get(pk=help_id)
	except Exception, e:
		print "unable to find help form!"
		print e
	return render_to_response('helpdesk/help_view.html', {'help': help}, context_instance=RequestContext(request))


def get_all(request):
	try:
		all_help = HelpRequest.objects.filter(status='answered')
	except Exception, e:
		print "Couldn't find all questions"
		print e
	return render_to_response('helpdesk/help_all_requests.html', {'form': all_help}, context_instance=RequestContext(request))


def get_pending(request):
	try:
		requests_pending = HelpRequest.objects.exclude(status='answered')
	except Exception, e:
		print "Couldn't find all pending questions"
		print e
	return render_to_response('helpdesk/pending_help.html', {'form': requests_pending}, context_instance=RequestContext(request))


def edit_help(request, help_id):
	try:
		help = HelpRequest.objects.get(pk=help_id)
	except Exception, e:
		print "Couldn't find question"
		print e
	if request.method == 'POST':
		helpform = HelpForm(request.POST, request.FILES, instance=help)
		try:
			help = helpform.save()
		except Exception, e:
			print e
		if help.id:
			redirect('helpdesk.views.get_help', help.id)
	else:
		helpform = HelpForm()
	return render_to_response('helpdesk/help_edit.html', {'form': helpform}, context_instance=RequestContext(request))


def admin_help(request, help_id):
	try:
		help = HelpRequest.objects.get(pk=help_id)
	except Exception, e:
		print e
		print "couldn't load help object"
	if request.method == 'POST':
		helpform = HelpFormComplete(request.POST, request.FILES, instance=help)
		try:
			help = helpform.save()
		except Exception, e:
			print e
		if help.id:
			redirect('helpdesk.views.get_help', help.id)
	else:
		helpform = HelpForm()
	return render_to_response('helpdesk/help_admin.html', {'form': helpform}, context_instance=RequestContext(request))
