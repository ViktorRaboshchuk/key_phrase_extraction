
from django import forms
from django.forms import Textarea

from data.models import Text, KeyPhrases


class TextForm(forms.ModelForm):

    class Meta:
        model = Text
        fields = ('text_area', 'time',)
        # fields = '__all__'
        widgets = {
            'text_area': Textarea(attrs={'cols': 150, 'rows': 25}),
        }


# class KeyPhrasesForm(forms.Form):
#
#     class Meta:
#         model = KeyPhrases
#         fields = ('phrases',)
#         widgets = {
#             'text_area': Textarea(attrs={'cols': 150, 'rows': 25}),
#         }