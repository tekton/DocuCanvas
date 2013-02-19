from django.db import models

from projects.models import Project, Section


class Node(models.Model):
    project = models.ForeignKey(Project)
    number = models.IntegerField(default=0)
    # created_by = models.ForeignKey(User)  # if the user is deleted I don't want this deleted though...
    section = models.ForeignKey(Section, blank=True, null=True)
    title = models.CharField(max_length=255)  # required for basic showing on page
    description = models.TextField(blank=True, null=True)
    slug_title = models.SlugField(blank=True, null=True)  # for direct linking!
    slug_description = models.SlugField(blank=True, null=True)  # for i'm not sure what yet...
    description_preview = models.CharField(max_length=255, blank=True, null=True)
    # short_description  # really should just be a truncate call

    def __unicode__(self):
        return "[" + str(self.project.name) + "] (" + str(self.number) + ") " + str(self.title)
