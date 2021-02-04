from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Text(models.Model):
    text_area = models.TextField(max_length=150000)
    time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return 'text number {}'.format(self.id)


class KeyPhrases(models.Model):
    key = models.ForeignKey(Text, on_delete= models.CASCADE)
    phrases = ArrayField(ArrayField(models.CharField(max_length=25500, blank=True, default=''), default=list,))

    def __str__(self):
        return 'key phrases # {}'.format(self.id)
