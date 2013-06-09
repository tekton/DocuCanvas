from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from django.forms.models import model_to_dict
from newsfeed.models import NewsFeedItem


class Checklist(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(Project)  # fk

    def __unicode__(self):
        return self.name


class CheckListLayoutItems(models.Model):
    Checklist = models.ForeignKey(Checklist)
    title = models.CharField(max_length=255)
    order = models.IntegerField()

    def save(self, user=None, commit=True, *args, **kwargs):
        if user:
            print "attempting to save layout item"
            # print dir(self)
            print "Title {0} and Order {1}".format(self.title, self.order)
            if not self.pk:  # for new items being created
                super(CheckListLayoutItems, self).save(*args, **kwargs)
                try:
                    news_feed_item = NewsFeedItem()
                    news_feed_item.user = user
                    news_feed_item.project = self.Checklist.project
                    news_feed_item.checklist = self.Checklist
                    news_feed_item.newsfeed_type = 'create_checklist_item'
                    news_feed_item.comment = 'new field ' + str(self.title)
                    news_feed_item.save()
                except Exception, e:
                    print e
            else:  # for updates to items
                try:
                    old_checklist_item = CheckListLayoutItems.objects.get(pk=self.pk)
                    if old_checklist_item.title != self.title:
                        f = "title"
                    elif old_checklist_item.order != self.order:
                        f = "order"
                    else:
                        f = None
                    super(CheckListLayoutItems, self).save(*args, **kwargs)
                    try:
                        news_feed_item = NewsFeedItem()
                        news_feed_item.user = user
                        news_feed_item.project = self.Checklist.project
                        news_feed_item.checklist = self.Checklist
                        news_feed_item.newsfeed_type = 'update_checklist_item'
                        try:
                            news_feed_item.field_change = 'checklist item'
                            if f == "title":
                                news_feed_item.old_value = old_checklist_item.title
                                news_feed_item.new_value = self.title
                            else:
                                news_feed_item.old_value = old_checklist_item.order
                                news_feed_item.new_value = self.order
                            news_feed_item.save()
                        except Exception, e:  # exception for the try to save news_feed_item
                            print e
                    except Exception, e:  # exception for the creation of news_feed_item
                        print e
                except Exception, e:  # exception for the get and save lines
                    print e
        else:
            print 'user was not given!'
            super(CheckListLayoutItems, self).save(*args, **kwargs)

        return self

    def __unicode__(self):
        return self.title


class ChecklistInstance(models.Model):
    checklist = models.ForeignKey(Checklist)  # fk
    title = models.CharField(max_length=255, blank=True, null=True)
    completion_status = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW

    def save(self, user=None, *args, **kwargs):
        new_checklist_instance = False
        if user:
            if not self.pk:
                new_checklist_instance = True
            else:
                old_checklist_instance = ChecklistInstance.objects.get(pk=self.pk)
        super(ChecklistInstance, self).save(*args, **kwargs)
        if user:
            try:
                news_feed_item = NewsFeedItem()
                news_feed_item.user = user
                news_feed_item.project = self.checklist.project
                news_feed_item.checklist = self.checklist
                if new_checklist_instance:
                    news_feed_item.newsfeed_type = 'create_checklist_instance'
                    news_feed_item.comment = self.pk
                    news_feed_item.save()
                else:
                    try:
                        if old_checklist_instance.title != self.title:
                            news_feed_item.newsfeed_type = 'update_checklist_instance'
                            news_feed_item.field_change = 'title'
                            news_feed_item.old_value = old_checklist.title
                            news_feed_item.new_value = self.title
                            news_feed_item.comment = self.pk
                            news_feed_item.save()
                        if old_checklist_instance.completion_status != self.completion_status:
                            news_feed_item.newsfeed_type = 'update_checklist_instance'
                            news_feed_item.field_change = 'completion_status'
                            news_feed_item.old_value = old_checklist_instance.completion_status
                            news_feed_item.new_value = self.completion_status
                            news_feed_item.comment = self.pk
                            news_feed_item.save()
                    except Exception, e:
                        print 'problem with old vs new checklist code'
                        print e
            except Exception, e:
                print 'problem with news feed item'
                print e
        return self

    def __unicode__(self):
        return self.title


class ChecklistTag(models.Model):
    checklist_instance = models.ForeignKey(ChecklistInstance)
    completion_status = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    modified = models.DateField(auto_now=True)  # auto update time
    modified_by = models.ForeignKey(User, null=True, blank=True)

    def save(self, user=None, *args, **kwargs):
        if user:
            if self.pk:
                try:
                    old_checklist_tag = ChecklistTag.objects.get(pk=self.pk)
                    super(ChecklistTag, self).save(*args, **kwargs)
                    try:
                        news_feed_item = NewsFeedItem()
                        news_feed_item.user = user
                        news_feed_item.project = self.checklist_instance.checklist.project
                        news_feed_item.checklist = self.checklist_instance.checklist
                        news_feed_item.newsfeed_type = 'update_checklist_instance_tag'
                        try:
                            if old_checklist_tag.completion_status != self.completion_status:
                                news_feed_item.field_change = 'completion_status'
                                news_feed_item.old_value = old_checklist_tag.completion_status
                                news_feed_item.new_value = self.completion_status
                                news_feed_item.description = self.checklist_instance.pk
                            if old_checklist_tag.name != self.name:
                                news_feed_item.field_change = 'name'
                                news_feed_item.old_value = old_checklist_tag.name
                                news_feed_item.new_value = self.name
                                news_feed_item.description = self.checklist_instance.pk
                            if old_checklist_tag.comment != self.comment:
                                news_feed_item.field_change = 'comment'
                                news_feed_item.old_value = old_checklist_tag.comment
                                news_feed_item.new_value = self.comment
                                news_feed_item.description = self.checklist_instance.pk
                            news_feed_item.save()
                        except Exception, e:
                            print e
                    except Exception, e:
                        print e
                except Exception, e:
                    print e
        else:
            print 'user was not given!'
            super(ChecklistTag, self).save(*args, **kwargs)

        return self

    def __unicode__(self):
        return self.name
