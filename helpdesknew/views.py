import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.forms.models import inlineformset_factory

from helpdesknew.forms import HelpForm, HelpFormResponse, ResponseFormValue, AckForm, HelpPhotoForm
from helpdesknew.models import HelpRequest, HelpResponse, HelpImageFile


@login_required
def help_form(request):
    photoFormset = inlineformset_factory(HelpRequest, HelpImageFile, can_delete=False, extra=1)
    helpRequest = HelpRequest()
    if request.method == 'POST':
        if 'add_help_screenshot' in request.POST:
            cp = request.POST.copy()
            cp['helpimagefile_set-TOTAL_FORMS'] = int(cp['helpimagefile_set-TOTAL_FORMS']) + 1
            formset = photoFormset(cp, request.FILES)
        elif 'submit' in request.POST:
            helpForm = HelpForm(request.POST, instance=helpRequest)
            formset = photoFormset(request.POST, request.FILES, instance=helpRequest)
            if helpForm.is_valid() and formset.is_valid():
                helpRequest = helpForm.save()
                formset.save()
                return redirect('helpdesknew.views.get_help', helpRequest.id)
    else:
        formset = photoFormset(instance=helpRequest)
    helpForm = HelpForm(instance=helpRequest)
    return render_to_response('helpdesknew/help_form.html', {'form': helpForm, 'photoset': formset}, context_instance=RequestContext(request))


@login_required
def get_help(request, help_id):
    try:
        help = HelpRequest.objects.get(pk=help_id)
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': "7"}, context_instance=RequestContext(request))
    try:
        images = HelpImageFile.objects.filter(helprequest=help)
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': "7"}, context_instance=RequestContext(request))
    try:
        comments = HelpResponse.objects.filter(helprequest=help).order_by('id')
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': "7"}, context_instance=RequestContext(request))
    try:
        answer = HelpResponse.objects.filter(helprequest=help).filter(value="('answer', 'Answer')")
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': "7"}, context_instance=RequestContext(request))
    try:
        help_response = HelpFormResponse(instance=HelpResponse(helprequest=help))
        help_form = HelpForm(instance=help)
    except Exception, e:
        print e
    return render_to_response('helpdesknew/help_view.html', {'help': help, 'form': help_form, 'help_response': help_response, 'comments': comments, 'answer': answer, 'images': images}, context_instance=RequestContext(request))


@login_required
def submit_response(request, help_id):
    try:
        help = HelpRequest.objects.get(pk=help_id)
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    help_me = HelpResponse(helprequest=help)
    if request.method == 'POST':
        try:
            form = HelpFormResponse(request.POST, instance=help_me)
            if form.is_valid():
                try:
                    help_me = form.save()
                except Exception, e:
                    return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
                state = help.status
                if state == '(1, 1)':
                    help.update_status(1)
                    help.save()
        except Exception, e:
            return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
    else:
        form = HelpFormRequest()
    return redirect('helpdesknew.views.get_help', help_id, permanent=False)


@login_required
def get_pending(request):
    try:
        requests_pending = HelpRequest.objects.exclude(status="('resolved', 'Resolved')").exclude(status="('closed', 'Closed')").order_by("-id")
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    return render_to_response('helpdesknew/pending_help.html', {'form': requests_pending}, context_instance=RequestContext(request))


@login_required
def get_resolved(request):
    try:
        resolved = HelpRequest.objects.filter(status="('resolved', 'Resolved')").order_by('-id')
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    try:
        closed = HelpRequest.objects.filter(status="('closed', 'Closed')").order_by('-id')
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    return render_to_response('helpdesknew/help_resolved.html', {'form': resolved, 'closed': closed}, context_instance=RequestContext(request))


@login_required
def user_help(request):
    try:
        requests_from_user = HelpRequest.objects.filter(user=request.user)
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    try:
        responses = requests_from_user.exclude(status="('resolved', 'Resolved')").exclude(status="('closed', 'Closed')").order_by("-id")
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    try:
        answers = requests_from_user.filter(status="('resolved', 'Resolved')").order_by('-id')
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    try:
        more_answers = requests_from_user.filter(status="('closed', 'Closed')").order_by('-id')
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    return render_to_response('helpdesknew/help_user.html', {'requests': requests_from_user, 'responses': responses, 'answers': answers, "myuser": request.user, "more_answers": more_answers}, context_instance=RequestContext(request))


@login_required
def error_page(request, error_id):
    return render_to_response('helpdesknew/error_page.html', {'error_id': error_id}, context_instance=RequestContext(request))


@login_required
def close_question(request, help_id):
    try:
        help = HelpRequest.objects.get(pk=help_id)
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    if request.method == 'POST':
        if help.status == "('resolved', 'Resolved')":
            try:
                help.update_status(4)
            except Exception, e:
                return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
            try:
                help.save()
            except Exception, e:
                return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
            return redirect('helpdesknew.views.get_help', help_id)
        elif help.status == "('closed', 'Closed')":
            try:
                help.update_status(2)
            except Exception, e:
                return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
            try:
                help.save()
            except Exception, e:
                return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
            return redirect('helpdesknew.views.get_help', help_id)
        else:
            return render_to_response('helpdesknew/error_page.html', {'error_id': '3'}, context_instance=RequestContext(request))
    return render_to_response('helpdesknew/close_question.html', {'help': help}, context_instance=RequestContext(request))


@login_required
def mark_the_answer(request, response_id):
    try:
        answer = HelpResponse.objects.get(pk=response_id)
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '7'}, context_instance=RequestContext(request))
    if request.method == 'POST':
        if answer.helprequest.status == "('resolved', 'Resolved')":
            return render_to_response('helpdesknew/error_page.html', {'error_id': '1'}, context_instance=RequestContext(request))
        elif answer.helprequest.status == "('closed', 'Closed')":
            return render_to_response('helpdesknew/error_page.html', {'error_id': '2'}, context_instance=RequestContext(request))
        else:
            answer.mark_answer()
            answer.helprequest.update_status(2)
            answer.save()
            answer.helprequest.save()
            return redirect('helpdesknew.views.get_help', answer.helprequest.id)
    return redirect('helpdesknew.views.get_help', answer.helprequest.id, permanent=False)


@login_required
def mark_the_input(request, response_id):
    try:
        answer = HelpResponse.objects.get(pk=response_id)
    except Exception, e:
        return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
    if request.method == 'POST':
        if answer.helprequest.status == "('closed', 'Closed')":
            return render_to_response('helpdesknew/error_page.html', {'error_id': '2'}, context_instance=RequestContext(request))
        else:
            answer.mark_input()
            answer.helprequest.update_status(3)
            answer.save()
            answer.helprequest.save()
            return redirect('helpdesknew.views.get_help', answer.helprequest.id)
    return redirect('helpdesknew.views.get_help', answer.helprequest.id, permanent=False)


@login_required
def edit_question(request, help_id):
    helpdeez = HelpRequest.objects.get(pk=help_id)
    if request.user.id == helpdeez.user.id:
        if helpdeez.status == "('closed', 'Closed')":
            return render_to_response('helpdesknew/error_page.html', {'error_id': '5'}, context_instance=RequestContext(request))
        if request.method == 'POST':
            help = HelpRequest.objects.get(pk=help_id)
            helpform = HelpForm(request.POST, instance=help)
            if helpform.is_valid():
                help.question_is_edit()
                try:
                    help = helpform.save()
                except Exception, e:
                    return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
                return redirect('helpdesknew.views.get_help', help.id)
        else:
            help = HelpRequest.objects.get(pk=help_id)
            helpform = HelpForm(instance=help)
        return render_to_response('helpdesknew/edit_question.html', {'help': help, 'form': helpform}, context_instance=RequestContext(request))
    else:
        return redirect('helpdesknew.views.get_help', help_id)


@login_required
def edit_comment(request, response_id):
    respondeez = HelpResponse.objects.get(pk=response_id)
    if request.user.id == respondeez.user.id:
        if respondeez.value == "('answer', 'Answer')":
            return render_to_response('helpdesknew/error_page.html', {'error_id': '4'}, context_instance=RequestContext(request))
        if request.method == 'POST':
            comment = HelpResponse.objects.get(pk=response_id)
            comment_form = HelpFormResponse(request.POST, instance=comment)
            if comment_form.is_valid():
                try:
                    comment = comment_form.save()
                except Exception, e:
                    return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
                return redirect('helpdesknew.views.get_help', comment.helprequest.id)
        else:
            comment = HelpResponse.objects.get(pk=response_id)
            comment_form = HelpFormResponse(instance=comment)
        return render_to_response('helpdesknew/edit_comment.html', {'comment': comment, 'form': comment_form}, context_instance=RequestContext(request))
    else:
        return redirect('helpdesknew.views.get_help', respondeez.helprequest.id)


@login_required
def ack_answer(request, response_id):
    answer = HelpResponse.objects.get(pk=response_id)
    if request.user.id == answer.helprequest.user.id:
        answer = HelpResponse.objects.get(pk=response_id)
        if request.method == 'POST':
            answer = HelpResponse.objects.get(pk=response_id)
            help = answer.helprequest
            helpform = AckForm(request.POST, instance=help)
            if helpform.is_valid():
                try:
                    help = helpform.save()
                except Exception, e:
                    return render_to_response('helpdesknew/error_page.html', {'error_id': '8'}, context_instance=RequestContext(request))
                return redirect('helpdesknew.views.get_help', answer.helprequest.id)
        else:
            answer = HelpResponse.objects.get(pk=response_id)
            help = answer.helprequest
            helpform = AckForm(instance=help)
        return render_to_response('helpdesknew/ack_answer.html', {'help': help, 'answer': answer, 'form': helpform}, context_instance=RequestContext(request))
    else:
        return redirect('helpdesknew.views.get_help', answer.helprequest.id)
