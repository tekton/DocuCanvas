from django import forms

from checklists.models import Checklist, ChecklistInstance,ChecklistTag, CheckListLayoutItems


'''
Forms for submitting bug reports and suggestions
'''
class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist

class CheckListLayoutItemsForm(forms.ModelForm):
    class Meta:
        model = CheckListLayoutItems

class ChecklistInstanceForm(forms.ModelForm):
    class Meta:
        model = ChecklistInstance
        fields = ('title',)

class ChecklistInstanceFullForm(forms.ModelForm):
    class Meta:
        model = ChecklistInstance

class ChecklistTagForm(forms.ModelForm):
    class Meta:
        model = ChecklistTag