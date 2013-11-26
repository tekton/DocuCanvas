from django.db import models
from django.contrib.auth.models import User

from projects.models import Project
from daily_reports.models import UserDailyReport

NEWSFEEDTYPE = (('update_issue', 'Update Issue'), ('create_issue', 'Create Issue'), ('comment', 'Comment'),
                    ('update_project', 'Update Project'), ('create_project', 'Create Project'), ('create_food_request', 'Create Food Request'),
                    ('complete_food_request', 'Complete Food Request'), ('create_checklist', 'Create Checklist'), ('update_checklist', 'Update Checklist'),
                    ('create_checklist_item', 'Create Checklist Item'), ('update_checklist_item', 'Update Checklist Item'), ('create_checklist_instance', 'Create Checklist Instance'),
                    ('update_checklist_instance', 'Update Checklist Instance'),('update_checklist_instance_tag', 'Update Checklist Instance Tag'), 
                    ('create_daily_report', 'Create Daily Report'))


class NewsFeedItem(models.Model):
    user = models.ForeignKey(User)  # fk
    issue = models.ForeignKey('issues.Issue', blank=True, null=True)  # fk
    project = models.ForeignKey(Project, blank=True, null=True)  # fk
    food = models.ForeignKey('food.FoodRequest', blank=True, null=True)  # fk
    checklist = models.ForeignKey('checklists.Checklist', blank=True, null=True)  # fk
    daily_report = models.ForeignKey(UserDailyReport, blank=True, null=True)  # fk
    comment = models.TextField(blank=True, null=True)
    field_change = models.CharField(max_length=255, blank=True, null=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    newsfeed_type = models.CharField(max_length=255, blank=True, null=True, choices=NEWSFEEDTYPE)
    timestamp = models.DateTimeField(auto_now_add=True)
