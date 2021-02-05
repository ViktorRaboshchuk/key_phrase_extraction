
from django import forms
from django.forms import Textarea

from data.models import Text


class TextForm(forms.ModelForm):

    class Meta:
        model = Text
        fields = ('text_area', 'time',)
        widgets = {
            'text_area': Textarea(attrs={'cols': 115, 'rows': 14}),
        }