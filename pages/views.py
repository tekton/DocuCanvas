from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect

def main(request):
	return render_to_response("pages/main.html", {}, context_instance=RequestContext(request))