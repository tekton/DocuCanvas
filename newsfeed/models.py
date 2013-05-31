from django.db import models
from django.contrib.auth.models import User

from projects.models import Project

NEWSFEEDTYPE = (('update_issue', 'Update Issue'), ('create_issue', 'Create Issue'), ('delete_issue', 'Delete Issue'), ('comment', 'Comment'),
                    ('update_project', 'Update Project'), ('create_project', 'Create Project'), ('delete_issue', 'Delete Project'))


class NewsFeedItem(models.Model):
    user = models.ForeignKey(User)  # fk
    issue = models.ForeignKey('issues.Issue', blank=True, null=True)  # fk
    project = models.ForeignKey(Project, blank=True, null=True)  # fk
    comment = models.CharField(max_length=255, blank=True, null=True)
    field_change = models.CharField(max_length=255, blank=True, null=True)
    old_value = models.CharField(max_length=255, blank=True, null=True)
    new_value = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=255)
    newsfeed_type = models.CharField(max_length=255, blank=True, null=True, choices=NEWSFEEDTYPE)
    timestamp = models.DateField(auto_now_add=True)
