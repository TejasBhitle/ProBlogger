from __future__ import unicode_literals

from django.db import models
from django.conf import settings


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width",
                              height_field="height")
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)

    # for python 2
    def __unicode__(self):
        return self.title

    # for python 3
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/posts/%s/" %(self.id)
