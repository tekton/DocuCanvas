from django.shortcuts import render_to_response
from django.template import RequestContext
from projects.models import *
from projects.forms import *


def project_form(request):
	if request.method == 'POST':
		pass
	else:
		form = ProjectForm()

	return render_to_response("projects/project_form.html", {'form':form}, context_instance=RequestContext(request))

def project_overview(request, project_name):

	print project_name
	project = Project.objects.get(name=project_name)

	return render_to_response("projects/project_overview.html", {'project':project}, context_instance=RequestContext(request))