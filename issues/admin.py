from django.contrib import admin

from issues.models import IssueHistorical, IssueStatusUpdate, IssueFieldUpdate

admin.site.register(IssueStatusUpdate)
admin.site.register(IssueFieldUpdate)
admin.site.register(IssueHistorical)
