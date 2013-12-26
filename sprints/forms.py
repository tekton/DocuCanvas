from django import forms
from django.forms import ModelForm
from models import Sprint

class SprintForm(forms.ModelForm):
	class Meta:
		model = Sprint
