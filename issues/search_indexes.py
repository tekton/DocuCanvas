from haystack import indexes
from issues.models import Issue, IssueComment
from projects.models import Project
#from daily_reports.models import *
from helpdesknew.models import *
from food.models import *
from notifications.models import *


class IssueIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    project = indexes.CharField(model_attr='project')
    #status = indexes.CharField(model_attr='status')
    created_by = indexes.CharField(model_attr='created_by')
    #assigned_to = indexes.CharField(model_attr='assigned_to')
    #type = indexes.CharField(model_attr='type', faceted=True)
    #location = indexes.CharField(model_attr='location', faceted=True)

    def get_model(self):
        return Issue

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class IssueCommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')

    def get_model(self):
        return IssueComment

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class HelpRequestIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')

    def get_model(self):
        return HelpRequest

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class HelpResponseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')

    def get_model(self):
        return HelpResponse

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class FoodRequestIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    total_cost = indexes.CharField(model_attr='total_cost')

    def get_model(self):
        return FoodRequest

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class NotificationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator')

    def get_model(self):
        return Notification

    def index_queryset(self, using=None):
        return self.get_model().objects.all()