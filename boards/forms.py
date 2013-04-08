from django import forms

from boards.models import Board, BoardNote, BoardNode


'''
Forms for submitting bug reports and suggestions
'''


class BoardsForm(forms.ModelForm):
    class Meta:
        model = Board


class BoardNoteForm(forms.ModelForm):
    class Meta:
        model = BoardNote


class BoardNodeForm(forms.ModelForm):
    class Meta:
        model = BoardNode
