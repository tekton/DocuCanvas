from haystack import indexes
from notifications.models import Notification


class NotificationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator')

    def get_model(self):
        return Notification

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
