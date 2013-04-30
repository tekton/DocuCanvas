from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from helpdesknew.forms import HelpForm, HelpFormResponse, ResponseFormValue
from helpdesknew.models import HelpRequest, HelpResponse


@login_required
def help_form(request):
    if request.method == 'POST':
        help = HelpRequest()
        helpform = HelpForm(request.POST, request.FILES, instance=help)
        try:
            help = helpform.save()
        except Exception, e:
            print "could not save help form"
            print e
        if help.id:
            return redirect('helpdesknew.views.get_help', help.id)
        else:
            print "something went wrong"
            print help
    else:
        helpform = HelpForm()
    return render_to_response('helpdesknew/help_form.html', {'form': helpform}, context_instance=RequestContext(request))


@login_required
def get_help(request, help_id):
    try:
        help = HelpRequest.objects.get(pk=help_id)
    except Exception, e:
        print "something went horribly horribly wrong"
        print e
    try:
        comments = HelpResponse.objects.filter(helprequest=help).order_by('-created')
    except Exception, e:
        print "couldn't find input objects"
    try:
        answer = HelpResponse.objects.filter(helprequest=help).filter(value="('answer', 'Answer')")
    except Exception, e:
        print "couldn't find answer objects"
    try:
        help_me = HelpResponse(helprequest=help)
        help_response = HelpFormResponse(instance=help_me)
        help_form = HelpForm(instance=help)
    except Exception, e:
        print e
    return render_to_response('helpdesknew/help_view.html', {'help': help, 'form': help_form, 'help_response': help_response, 'comments': comments, 'answer': answer}, context_instance=RequestContext(request))


@login_required
def submit_response(request, help_id):
    try:
        help = HelpRequest.objects.get(pk=help_id)
    except Exception, e:
        print e
    try:
        help_response = HelpResponse.objects.filter(helprequest=help).order_by('-value')
    except Exception, e:
        print e
    help_me = HelpResponse(helprequest=help)
    if request.method == 'POST':
        try:
            form = HelpFormResponse(request.POST, instance=help_me)
            if form.is_valid():
                try:
                    help_me = form.save()
                except Exception, e:
                    print e
                    print "couldn't validate comment"
                state = help.status
                if state == '(1, 1)':
                    help.update_status(1)
                    help.save()
                    print "updated object saved"
                else:
                    print help.status
            else:
                print "fix your form"
        except Exception, e:
            print e
            print "couldn't create comment"
    else:
        form = HelpFormRequest()
    return redirect('helpdesknew.views.get_help', help_id, permanent=False)


@login_required
def get_all(request):
    try:
        all_help = HelpRequest.objects.all()
    except Exception, e:
        print "Couldn't find all questions"
        print e
    return render_to_response('helpdesknew/help_all_requests.html', {'form': all_help}, context_instance=RequestContext(request))


@login_required
def get_pending(request):
    try:
        requests_pending = HelpRequest.objects.exclude(status="('resolved', 'Resolved')")
    except Exception, e:
        print "Couldn't find all pending questions"
        print e
    return render_to_response('helpdesknew/pending_help.html', {'form': requests_pending}, context_instance=RequestContext(request))


@login_required
def get_resolved(request):
    try:
        resolved = HelpRequest.objects.filter(status="('resolved', 'Resolved')").order_by('-request_init')
    except Exception, e:
        print e
    return render_to_response('helpdesknew/help_resolved.html', {'form': resolved}, context_instance=RequestContext(request))


@login_required
def mark_as_answer(request, response_id):
    try:
        answer = HelpResponse.objects.get(pk=response_id)
        print "it works the first time around"
    except Exception, e:
        print e
        print "no answer"
    try:
        answers = HelpResponse.objects.filter(helprequest=answer.helprequest)
    except Exception, e:
        print e
    if request.method == 'POST':
        response_form = ResponseFormValue(request.POST, instance=answer)
        if request.POST['value'] == 'answer':
            answer.mark_answer()
            try:
                answer.save()
            except Exception, e:
                print "answer didn't save"
            help = HelpRequest.objects.get(pk=answer.helprequest.id)
            help.update_status(2)
            help.save()
        else:
            answer.mark_input()
            try:
                answer.save()
            except Exception, e:
                print "input didn't save"
            help = HelpRequest.objects.get(pk=answer.helprequest.id)
            if help.status == "('resolved', 'Resolved')":
                help.update_status(3)
            else:
                help.update_status(1)
            help.save()
        if answer.id:
            help_id = answer.helprequest.id
            return redirect('helpdesknew.views.get_help', help_id)
    else:
        response_form = ResponseFormValue(instance=answer)
    return render_to_response('helpdesknew/mark_as_answer.html', {'response': answer, 'response_form': response_form}, context_instance=RequestContext(request))


@login_required
def user_help(request, user_id):
    try:
        myuser = User.objects.get(pk=user_id)
    except Exception, e:
        print e
        print "no myuser object"
    try:
        requests_from_user = HelpRequest.objects.filter(user=myuser)
    except Exception, e:
        print e
        print "couldn't find user questions"
    return render_to_response('helpdesknew/help_user.html', {'requests': requests_from_user}, context_instance=RequestContext(request))
