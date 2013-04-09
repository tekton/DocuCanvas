from django.contrib import admin

from models import *
from projects.models import *
from issues.models import *
from accounts.models import *
from boards.models import *

admin.site.register(Node)
admin.site.register(Project)
admin.site.register(Account)
admin.site.register(Section)
admin.site.register(Issue)
admin.site.register(MetaIssue)
admin.site.register(IssueComment)
admin.site.register(SubscriptionToIssue)
admin.site.register(PinToIssue)
admin.site.register(Board)
admin.site.register(BoardNote)
admin.site.register(BoardNode)