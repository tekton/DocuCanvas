from django.contrib import admin

from issues.models import IssueHistorical, IssueStatusUpdate, IssueFieldUpdate, ProjectPlannerItem, ProjectPlannerItemConnection

admin.site.register(IssueStatusUpdate)
admin.site.register(IssueFieldUpdate)
admin.site.register(IssueHistorical)
admin.site.register(ProjectPlannerItem)
admin.site.register(ProjectPlannerItemConnection)
