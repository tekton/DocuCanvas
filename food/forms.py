from django import forms
from food.models import FoodRequest
from newsfeed.models import *

class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodRequest


class FoodFormTres(forms.ModelForm):
    class Meta:
        model = FoodRequest
        fields = ('item', 'quantity', 'quantity_type', 'cost_per_quantity', 'user', 'desired_completion')

    def save(self, user=None, *args, **kwargs):
        super(FoodFormTres, self).save(*args, **kwargs)
        if user:
            try:
                newsfeed = NewsFeedItem()
                newsfeed.user = user
                newsfeed.food = self.instance
                newsfeed.newsfeed_type = 'create_food_request'
                newsfeed.save()
            except Exception, e:
                print 'Unable to save new food form'
                print e
        return self.instance

class FoodFormComplete(forms.ModelForm):
    class Meta:
        model = FoodRequest
