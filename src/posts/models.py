from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # for python 2
    def __unicode__(self):
        return self.title

    # for python 3
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/posts/%s/" %(self.id)