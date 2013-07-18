from haystack import indexes
from issues.models import Issue, IssueComment


class IssueIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    project = indexes.CharField(model_attr='project')

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
