from django.db import models

# Create your models here.

class Text(models.Model):
    sentence = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.sentence[:10]