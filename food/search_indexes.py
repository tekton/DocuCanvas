from haystack import indexes
from food.models import FoodRequest


class FoodRequestIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    total_cost = indexes.CharField(model_attr='total_cost')

    def get_model(self):
        return FoodRequest

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
