from haystack import indexes
from helpdesknew.models import HelpRequest, HelpResponse


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
