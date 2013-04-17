from django import forms
from boards.models import Board, BoardNote, BoardNode


'''
Forms for submitting bug reports and suggestions
'''


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ('height', 'width',)


class BoardNoteForm(forms.ModelForm):
    class Meta:
        model = BoardNote


class BoardNodeForm(forms.ModelForm):
    class Meta:
        model = BoardNode
