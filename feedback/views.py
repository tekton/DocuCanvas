# Create your views here.
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from projects.models import Project
from feedback.models import AnonymousFeedback, SignedFeedback, Feedback
from feedback.forms import AnonymousForm, SignedForm


@login_required
def feedback(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		raise e
	return render_to_response('feedback/feedback_form.html', {'projects': projects}, context_instance=RequestContext(request))


@login_required
def submit_feedback(request):
	if request.method == 'POST':
		print request.POST
		if request.POST.has_key('anonymous_toggle'):
			try:
				feedback = AnonymousFeedback()
				feedback.feedback = request.POST['feedback-description']
				feedback.save()
				return redirect('feedback.views.anonymous_view', feedback.id)
			except Exception, e:
				raise e
		else:
			try:
				feedback = SignedFeedback()
				feedback.feedback = request.POST['feedback-description']
				feedback.user = request.user
				feedback.save()
				return redirect('feedback.views.signed_view', feedback.id)
			except Exception, e:
				raise e
	return redirect('feedback.views.feedback')


@login_required
def anonymous_view(request, feedback_id):
	if request.user.is_staff:
		try:
			projects = Project.objects.all()
		except Exception, e:
			print e
		try:
			feedback = AnonymousFeedback.objects.get(pk=feedback_id)
		except Exception, e:
			print e
		return render_to_response('feedback/anonymous_view.html', {'projects': projects, 'anonymous': feedback}, context_instance=RequestContext(request))
	else:
		return redirect('feedback.views.all_signed')


@login_required
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


@login_required
def all_anonymous(request):
	if request.user.is_staff:
		try:
			projects = Project.objects.all()
		except Exception, e:
			print e
		try:
			feedback = AnonymousFeedback.objects.all()
		except Exception, e:
			print e
		return render_to_response('feedback/anonymous_all.html', {'projects': projects, 'anonymous': feedback}, context_instance=RequestContext(request))
	else:
		return redirect('feedback.views.all_signed')


@login_required
def all_signed(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		feedback = SignedFeedback.objects.all()
	except Exception, e:
		print e
	return render_to_response('feedback/signed_all.html', {'projects': projects, 'signed': feedback}, context_instance=RequestContext(request))


@login_required
def recordFeedback(request):
	to_json = {"success": True}
	try:
		referrer = request.META["HTTP_REFERER"]
	except Exception, e:
		to_json["success"] = False
		to_json["error_message"] = "HTTP Referer could not be retrieved"
	try:
		data = request.POST["data"]
	except Exception, e:
		to_json["success"] = False
		to_json["error_message"] = "POST data required"
	try:
		feedback = Feedback(page=referrer, feedback=data, user=request.user)
		feedback.save()
	except Exception, e:
		to_json["success"] = False
		to_json["error_message"] = "Database Failure"
	return HttpResponse(json.dumps(to_json), content_type='application/json')
