from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect

def main(request,pagename):
	filepath = "docs/"

	page = "main.html"
	if pagename:
		page = str(pagename) + ".html"
		
	filepath = filepath + page

	return render_to_response(filepath, {}, context_instance=RequestContext(request))