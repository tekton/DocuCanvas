from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)  # should really default to a slugified name


class Section(models.Model):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
