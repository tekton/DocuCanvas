from django import forms

from checklists.models import Checklist, ChecklistInstance,ChecklistTag


'''
Forms for submitting bug reports and suggestions
'''
class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist

class ChecklistInstanceForm(forms.ModelForm):
    class Meta:
        model = ChecklistInstance
        fields = ('title',)

class ChecklistTagForm(forms.ModelForm):
    class Meta:
        model = ChecklistTag


