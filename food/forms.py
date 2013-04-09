from django import forms
from food.models import FoodRequest


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodRequest
