# Create your views here.
from projects.models import Project
from issues.models import Issue, IssueComment
from helpdesknew.models import HelpRequest, HelpResponse



def search(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		raise e