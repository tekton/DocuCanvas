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


class FoodFormComplete(forms.ModelForm):
    class Meta:
        model = FoodRequest
