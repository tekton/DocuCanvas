from django.db import models
from django.contrib.auth.models import User


PROJECT_STATUS = (("on_time", "On Time"), ("at_risk", "At Risk"), ("late", "Late"), ("cancelled", "Cancelled"), ("on_hold", "On Hold"), ("not_started", "Not Started"),)
PROJECT_PHASE = (("define", "Define"), ("design", "Design"), ("implementation", "Implementation"), ("sustain", "Sustain"), ("ongoing", "Ongoing"), ("cancelled", "Cancelled"),)

class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)  # should really default to a slugified name
    #
    description = models.TextField(blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    business_case = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=0, blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    internal_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True, choices=PROJECT_STATUS)
    logo = models.CharField(max_length=255, blank=True, null=True)  # uri
    product_owner = models.ForeignKey(User, related_name='product_owner', blank=True, null=True)
    project_manager = models.ForeignKey(User, related_name='project_manager', blank=True, null=True)
    lead_developer = models.ForeignKey(User, related_name='lead_developer', blank=True, null=True)
    #
    potential_end_date = models.DateField(null=True, blank=True)  # calculated from tasks, features- bugs are backlog
    #
    current_phase = models.CharField(max_length=255, blank=True, null=True, choices=PROJECT_PHASE)
    phase_planning_start = models.DateField(null=True, blank=True)
    phase_planning_end = models.DateField(null=True, blank=True)
    phase_research_start = models.DateField(null=True, blank=True)
    phase_research_end = models.DateField(null=True, blank=True)
    #
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True, null=True, blank=True)  # auto update time
    #
    repository_url = models.CharField(max_length=255, blank=True, null=True)  # where to check in github or internal server
    deployment_server = models.CharField(max_length=255, blank=True, null=True)  # url for test environment
    deployment_url = models.CharField(max_length=255, blank=True, null=True)  # url of live environment
    #
    code_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
    # TODO etc


class Section(models.Model):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)

"""
class Product(models.Model):
    product = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    scope = models.TextField(blank=True,null=True)
    business_case = models.TextField(blank=True,null=True)
    priority = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=255, choices=PRODUCT_STATUS,default=PRODUCT_STATUS[0][0])
    #
    def __unicode__(self):
        return self.product
"""
