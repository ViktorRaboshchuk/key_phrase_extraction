from django import forms
from django.contrib import admin

# Register your models here.
from django.db import models
from django.forms import TextInput, Textarea

from data.forms import TextForm
from data.models import Text, KeyPhrases

admin.site.register(Text)
admin.site.register(KeyPhrases)

# class TextAdmin(admin.ModelAdmin):
#     form = TextForm
#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows':15, 'cols':140})},
#     }


# admin.site.register(Text, TextAdmin)
