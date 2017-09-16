from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from posts.models import Post


# Create your models here.
class CommentManager(models.Manager):
    def filter_by_instance(self, instance):

        # specific
        # content_type = ContentType.objects.get_for_model(Post)

        # dynamic for getting class
        content_type = ContentType.objects.get_for_model(instance.__class__)

        obj_id = instance.id
        queryset = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return queryset


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    # post = models.ForeignKey(Post)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username
