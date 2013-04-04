from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from projects.models import *
from projects.forms import *
from issues.models import *

def home(request):
    return render_to_response("dashboard.html", {}, context_instance=RequestContext(request))