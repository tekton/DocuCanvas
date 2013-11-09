from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from newsfeed.models import NewsFeedItem
# from django.utils.translation import ugettext as _
from projects.models import Project
from django.contrib import admin
from tinymce.models import HTMLField

import datetime

ISSUETOISSUETYPE = (('duplicated', 'Duplicate'), ('related', 'Related'), ('child', 'Child'), ('parent', 'Parent'))
ISSUETYPE = (("bug", "Bug"), ("task", "Task"), ("suggestion", "Suggestion"))
BUGSTATE = (("not_a_bug", "Not a bug"), ("wont_fix", "Won't Fix"), ("duplicate", "Duplicate"), ("active", "Active"), ("fixed", "Fixed"), ("retest", "Retest"), ("unverified", "Unverified"))


class MetaIssue(models.Model):
    project = models.ForeignKey(Project)  # fk
    # info
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField(default=0)
    # Meta Issue Type
    mi_type = models.CharField(max_length=255, choices=(('feature', 'Feature'), ('milestone', 'Milestone')))
    #
    user_story = models.TextField()
    #
    code_name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.title


class Issue(models.Model):
    project = models.ForeignKey(Project)  # fk
    meta_issues = models.ForeignKey(MetaIssue, null=True, blank=True)  # fk
    state = models.CharField(max_length=255, blank=True, null=True)  # list
    # dates
    projected_start = models.DateField(null=True, blank=True)
    projected_end = models.DateField(null=True, blank=True)
    actual_start = models.DateField(null=True, blank=True)
    actual_end = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    estimated_time = models.IntegerField(null=True, blank=True)
    #
    date_reported = models.DateField(null=True, blank=True)
    #
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True)  # auto update time
    #
    view_type = models.CharField(max_length=255, blank=True, null=True)  # default via name, or Issue ID
    #
    issue_type = models.CharField(max_length=255, blank=True, null=True, choices=ISSUETYPE)  # bug, task, suggestion
    #
    assigned_to = models.ForeignKey(User, blank=True, null=True, related_name='assigned_to')
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='created_by', editable=False)
    point_of_contact = models.ForeignKey(User, blank=True, null=True, related_name='poc')
    modified_by = models.ForeignKey(User, blank=True, null=True, related_name='modified_by')
    # basic information
    title = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=140, default="No Summary")
    description = models.TextField(null=True, blank=True)
    link_slug = models.SlugField(null=True, blank=True)
    # bug centric
    status = models.CharField(max_length=255, blank=True, null=True, choices=BUGSTATE)
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

    def __unicode__(self):
        return str(self.id)

    def save(self, user=None, *args, **kwargs):
        if self.pk:
            if user:
                try:
                    old_issue = Issue.objects.get(pk=self.id)

                    for field in self._meta.fields:
                        if getattr(self, field.attname) != getattr(old_issue, field.attname):
                            try:
                                ### create issue field update object if field changed
                                issue_field_update = IssueFieldUpdate()
                                issue_field_update.issue = self
                                issue_field_update.user = user
                                issue_field_update.field = field.attname
                                issue_field_update.old_value = getattr(old_issue, field.attname)
                                issue_field_update.new_value = getattr(self, field.attname)
                                issue_field_update.save()

                                ### create a newsfeed item for this status update
                                try:
                                    news_feed_item = NewsFeedItem()
                                    news_feed_item.user = user
                                    news_feed_item.issue = self
                                    news_feed_item.project = self.project
                                    news_feed_item.field_change = field.attname
                                    news_feed_item.old_value = getattr(old_issue, field.attname)
                                    news_feed_item.new_value = getattr(self, field.attname)
                                    news_feed_item.newsfeed_type = "update_issue"
                                    news_feed_item.save()
                                except e:
                                    print e
                            except Exception, e:
                                print 'couldnt save status update'
                                print e

                            if field.attname == 'status':
                                if self.status != old_issue.status:
                                    try:
                                        ### create issue status update object if status changed
                                        issue_status_update = IssueStatusUpdate()
                                        issue_status_update.issue = self
                                        issue_status_update.user = user
                                        issue_status_update.old_status = old_issue.status
                                        issue_status_update.new_status = self.status
                                        issue_status_update.save()
                                    except Exception, e:
                                        print 'couldnt save status update'
                                        print e

                    if self.status == 'fixed':
                        self.actual_end = datetime.date.today()
                    if self.status == 'active':
                        self.actual_start = datetime.date.today()
                except Exception, e:
                    print 'couldnt get old issue'
                    print e

            ### create historical issue object based on this new change
            try:
                issue_historical = IssueHistorical()
                issue_historical.issue = self
                for field in self._meta.fields:
                    if field.attname != 'id':
                        setattr(issue_historical, field.attname, getattr(self, field.attname))
                issue_historical.save()
            except Exception, e:
                'couldnt save historical issue'
                print e

            #try:
            #    update_index.Command().handle()
            #except Exception, e:
            #    print 'unable to update index'
            #    print e
        # go through list of assign/subscribed and put in a dictionary, loop through dictionary and queue an e-mail in celery
        super(Issue, self).save()



class IssueHistorical(models.Model):
    issue = models.ForeignKey(Issue, null=True, blank=True)
    project = models.ForeignKey(Project)  # fk
    meta_issues = models.ForeignKey(MetaIssue, null=True, blank=True)  # fk
    state = models.CharField(max_length=255, blank=True, null=True)  # list
    # dates
    projected_start = models.DateField(null=True, blank=True)
    projected_end = models.DateField(null=True, blank=True)
    actual_start = models.DateField(null=True, blank=True)
    actual_end = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    #
    date_reported = models.DateField(null=True, blank=True)
    #
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True)  # auto update time
    #
    view_type = models.CharField(max_length=255, blank=True, null=True)  # default via name, or Issue ID
    #
    issue_type = models.CharField(max_length=255, blank=True, null=True, choices=ISSUETYPE)  # bug, task, suggestion
    #
    assigned_to = models.ForeignKey(User, blank=True, null=True, related_name='assigned_to_history')
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='created_by_history', editable=False)
    point_of_contact = models.ForeignKey(User, blank=True, null=True, related_name='poc_history')
    modified_by = models.ForeignKey(User, blank=True, null=True, related_name='modified_by_history')
    # basic information
    title = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=140, default="No Summary")
    description = models.TextField(null=True, blank=True)
    link_slug = models.SlugField(null=True, blank=True)
    # bug centric
    status = models.CharField(max_length=255, blank=True, null=True, choices=BUGSTATE)
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

    def __unicode__(self):
        return 'Issue ' + str(self.issue) + ':' + self.description + ':' + str(self.modified)

'''
class FinishedIssue(models.Model):
    finished_issue = models.ForeignKey(Issue) #fk
    status = models.CharField(max_length=255, blank=True, null=True, choices=BUGSTATE)
'''


class IssueFieldUpdate(models.Model):
    issue = models.ForeignKey(Issue)  # fk
    user = models.ForeignKey(User)  # fk
    field = models.CharField(max_length=255, blank=True, null=True)
    old_value = models.CharField(max_length=255, blank=True, null=True)
    new_value = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(auto_now_add=True)


class IssueStatusUpdate(models.Model):
    issue = models.ForeignKey(Issue)  # fk
    user = models.ForeignKey(User)  # fk
    old_status = models.CharField(max_length=255, blank=True, null=True, choices=BUGSTATE)
    new_status = models.CharField(max_length=255, blank=True, null=True, choices=BUGSTATE)
    time_stamp = models.DateField(auto_now_add=True)


class IssueView(models.Model):
    issue = models.ForeignKey(Issue)  # fk
    hash_val = models.CharField(max_length=255)  # MD5 hash of something
    # bools for every value in the issues model...


class IssueToIssue(models.Model):
    primary_issue = models.ForeignKey(Issue, related_name='primary_issue')  # fk back to issue
    secondary_issue = models.ForeignKey(Issue, related_name='secondary_issue')  # fk back to issue
    link_type = models.CharField(max_length=255, choices=ISSUETOISSUETYPE, default='related')  # list of link types

    # class Meta:
    #    verbose_name = _('IssueToIssue')
    #    verbose_name_plural = _('IssueToIssues')

    def __unicode__(self):
        return str(self.primary_issue.summary) + ' ' + str(self.link_type) + ' ' + str(self.secondary_issue.summary)


class SubscriptionToIssue(models.Model):
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(User)
    communication_type = models.CharField(max_length=255, default="email")
    # if not e-mail, what?!
    communication_channel = models.CharField(max_length=255, blank=True, null=True)  # phone number, or? -- facebook, twitter, etc

    def __unicode__(self):
        return "{0} :: {1}".format(self.issue.id, self.user.username)

class PinIssue(models.Model):
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(User)


class IssueComment(models.Model):
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=255, blank=False)  # note: do not use the word 'text' as a field name

    def save(self, user=None, *args, **kwargs):
        if user:
            try:
                news_feed_item = NewsFeedItem()
                news_feed_item.user = user
                news_feed_item.issue = self.issue
                news_feed_item.project = self.issue.project
                news_feed_item.comment = self.description
                news_feed_item.newsfeed_type = 'comment'
                news_feed_item.save()
            except Exception, e:
                print e
        super(IssueComment, self).save(*args, **kwargs)


class IssueScreenshot(models.Model):
    issue = models.ForeignKey(Issue)
    screenshot = models.ImageField(upload_to="upload/issues", blank=True, null=True)


class ProjectPlannerItem(models.Model):
    project = models.ForeignKey(Project)
    meta_issue = models.ForeignKey(MetaIssue)
    item_type = models.CharField(max_length=255,blank=True, null=True, default="meta_issue")
    x_coordinate = models.IntegerField(default=0)
    y_coordinate = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.meta_issue.title)


class ProjectPlannerItemConnection(models.Model):
    project = models.ForeignKey(Project)
    source = models.ForeignKey(ProjectPlannerItem, related_name='source')
    target = models.ForeignKey(ProjectPlannerItem, related_name='target')
    def __unicode__(self):
        return str(self.source.meta_issue.title) + ' -> ' + str(self.target.meta_issue.title)

admin.site.register(IssueScreenshot)
