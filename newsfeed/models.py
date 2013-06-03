from django.db import models
from django.contrib.auth.models import User

from projects.models import Project


class NewsFeedItem(models.Model):
    user = models.ForeignKey(User)  # fk
    issue = models.ForeignKey('issues.Issue', blank=True, null=True)  # fk
    project = models.ForeignKey(Project, blank=True, null=True)  # fk
    description = models.TextField(blank=True, null=True, max_length=255)
    timestamp = models.DateField(auto_now_add=True)
