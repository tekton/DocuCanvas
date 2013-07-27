from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse

from projects.models import *

import json

@login_required
def test(request):
    return render_to_response("charts/test01.html", {}, context_instance=RequestContext(request))


@login_required
def home(request):
    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'

    return render_to_response("charts/charts.html", {"projects": projects}, context_instance=RequestContext(request))
