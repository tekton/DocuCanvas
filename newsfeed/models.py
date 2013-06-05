from django.db import models
from django.contrib.auth.models import User

from projects.models import Project
from food.models import FoodRequest
from checklists.models import Checklist
from daily_reports.models import UserDailyReport

NEWSFEEDTYPE = (('update_issue', 'Update Issue'), ('create_issue', 'Create Issue'), ('comment', 'Comment'),
                    ('update_project', 'Update Project'), ('create_project', 'Create Project'), ('create_food_request', 'Create Food Request'),
                    ('create_checklist', 'Create Checklist'),('create_daily_report','Create Daily Report'))


class NewsFeedItem(models.Model):
    user = models.ForeignKey(User)  # fk
    issue = models.ForeignKey('issues.Issue', blank=True, null=True)  # fk
    project = models.ForeignKey(Project, blank=True, null=True)  # fk
    food = models.ForeignKey(FoodRequest, blank=True, null=True)  # fk
    checklist = models.ForeignKey(Checklist, blank=True, null=True)  # fk
    daily_report = models.ForeignKey(UserDailyReport, blank=True, null=True)  # fk
    comment = models.CharField(max_length=255, blank=True, null=True)
    field_change = models.CharField(max_length=255, blank=True, null=True)
    old_value = models.CharField(max_length=255, blank=True, null=True)
    new_value = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=255)
    newsfeed_type = models.CharField(max_length=255, blank=True, null=True, choices=NEWSFEEDTYPE)
    timestamp = models.DateField(auto_now_add=True)