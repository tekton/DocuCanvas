from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.


def TestIndex(request):
    project = "DocuCanvas"
    page_type = "Bug Report"
    return render_to_response("test_templates/test_ui.html", {"project": project, "page_type": page_type}, context_instance=RequestContext(request))
