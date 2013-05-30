from django.contrib import admin

from issues.models import IssueHistorical, IssueStatusUpdate

admin.site.register(IssueStatusUpdate)
admin.site.register(IssueHistorical)
