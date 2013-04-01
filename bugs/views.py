from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.


def TestIndex(request):
    return render_to_response("test_templates/test_ui.html", {}, context_instance=RequestContext(request))
