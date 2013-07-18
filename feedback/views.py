# Create your views here.
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import Project
from feedback.models import AnonymousFeedback, SignedFeedback
from feedback.forms import AnonymousForm, SignedForm


def anonymous_feedback(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	feedback = AnonymousFeedback()
	if request.method == 'POST':
		form = AnonymousForm(request.POST, instance=feedback)
		if form.is_valid():
			try:
				feedback = form.save()
			except Exception, e:
				print "feedback form did not save"
			return redirect('feedback.views.anonymous_view', feedback.id)
	else:
		form = AnonymousForm()
	return render_to_response('feedback/anonymous_form.html', {'form': form, 'feedback': feedback, 'projects': projects}, context_instance=RequestContext(request))


def signed_feedback(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	feedback = SignedFeedback()
	if request.method == 'POST':
		form = SignedForm(request.POST, instance=feedback)
		if form.is_valid():
			try:
				feedback = form.save()
			except Exception, e:
				print "feedback form did not save"
			return redirect('feedback.views.signed_view', feedback.id)
	else:
		form = SignedForm()
	return render_to_response('feedback/signed_form.html', {'form': form, 'feedback': feedback, 'projects': projects}, context_instance=RequestContext(request))


def anonymous_view(request, feedback_id):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		feedback = AnonymousFeedback.objects.get(pk=feedback_id)
	except Exception, e:
		print e
	return render_to_response('feedback/anonymous_view.html', {'projects': projects, 'anonymous': feedback}, context_instance=RequestContext(request))


def signed_view(request, feedback_id):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		feedback = SignedFeedback.objects.get(pk=feedback_id)
	except Exception, e:
		print e
	return render_to_response('feedback/signed_view.html', {'projects': projects, 'signed': feedback}, context_instance=RequestContext(request))


def all_anonymous(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		feedback = AnonymousFeedback.objects.all()
	except Exception, e:
		print e
	return render_to_response('feedback/anonymous_all.html', {'projects': projects, 'anonymous': feedback}, context_instance=RequestContext(request))


def all_signed(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		feedback = SignedFeedback.objects.all()
	except Exception, e:
		print e
	return render_to-resposne('feedback/signed_all.html', {'projects': projects, 'sigend': feedback}, context_instance=RequestContext(request))