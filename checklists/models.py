from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Checklist(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(Project)  # fk

    def __unicode__(self):
        return self.name


class CheckListLayoutItems(models.Model):
    Checklist = models.ForeignKey(Checklist)
    title = models.CharField(max_length=255)
    order = models.IntegerField()

    def __unicode__(self):
        return self.title


class ChecklistInstance(models.Model):
    checklist = models.ForeignKey(Checklist)  # fk
    title = models.CharField(max_length=255, blank=True, null=True)
    completion_status = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW

    def __unicode__(self):
        return self.title


class ChecklistTag(models.Model):
    checklist_instance = models.ForeignKey(ChecklistInstance)
    completion_status = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    modified = models.DateField(auto_now=True)  # auto update time
    modified_by = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.name
