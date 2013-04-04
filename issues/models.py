from django.db import models
from django.contrib.auth.models import User

from projects.models import Project


class MetaIssue(models.Model):
    project = models.ForeignKey(Project)  # fk
    # info
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField(default=0)
    #
    mi_type = models.CharField(max_length=255)  # Meta Issue Type: feature, milestone, etc
    #
    user_story = models.TextField()


class Issue(models.Model):
    project = models.ForeignKey(Project)  # fk
    meta_issues = models.ForeignKey(MetaIssue)  # fk
    state = models.CharField(max_length=255, blank=True, null=True)  # list
    # dates
    projected_start = models.DateField(null=True, blank=True)
    projected_end = models.DateField(null=True, blank=True)
    actual_start = models.DateField(null=True, blank=True)
    actual_end = models.DateField(null=True, blank=True)
    #
    date_reported = models.DateField(null=True, blank=True)
    #
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True)  # auto update time
    #
    view_type = models.CharField(max_length=255, blank=True, null=True)  # default via name, or Issue ID
    #
    issue_type = models.CharField(max_length=255, blank=True, null=True)  # bug, task, suggestion
    #
    assigned_to = models.ForeignKey(User)
    # basic information
    title = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=140, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    link_slug = models.SlugField(null=True, blank=True)
    # bug centric
    status = models.CharField(max_length=255, blank=True, null=True)
    criticality = models.IntegerField(default=0, blank=True, null=True)
    priority = models.IntegerField(default=0, blank=True, null=True)
    fixability = models.CharField(max_length=255, blank=True, null=True)
    # tasks and suggestions
    r_and_d = models.CharField(max_length=255, blank=True, null=True)  # i don't remember what this is for...
    feature = models.CharField(max_length=255, blank=True, null=True)  # foreign key to something?
    # bug_resolution  # um...
    # random important information...
    os = models.CharField(max_length=255, blank=True, null=True)  # operating system
    os_version = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    browser_version = models.CharField(max_length=255, blank=True, null=True)
    screen_shot = models.CharField(max_length=255, blank=True, null=True)
    wireframe = models.CharField(max_length=255, blank=True, null=True)  # for suggestions, tasks, features, etc
    uri_to_test = models.CharField(max_length=255, blank=True, null=True)  # where they're having the issue


class IssueView(models.Model):
    issue = models.ForeignKey(Issue)  # fk
    hash_val = models.CharField(max_length=255)  # MD5 hash of something
    # bools for every value in the issues model...


class IssueToIssue(models.Model):
    primary_issue = models.ForeignKey(Issue, related_name='primary_issue')  # fk back to issue
    secondary_issue = models.ForeignKey(Issue, related_name='secondary_issue')  # fk back to issue
    link_type = models.CharField(max_length=255)  # list of link types
    """
    class Meta:
        verbose_name = _('IssueToIssue')
        verbose_name_plural = _('IssueToIssues')

    def __unicode__(self):
        pass
    """


class SubscriptionToIssue(models.Model):
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(User)
    communication_type = models.CharField(max_length=255, default="email")
    # if not e-mail, what?!
    communication_channel = models.CharField(max_length=255, blank=True, null=True)  # phone number, or? -- facebook, twitter, etc
