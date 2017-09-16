from django.conf.urls import url

from .views import (post_list, post_create,
                    post_detail, post_edit,
                    post_delete,my_post_list)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^my/$',my_post_list),
    url(r'^create/$', post_create),
    url(r'^(?P<post_id>\d+)/$', post_detail),
    url(r'^(?P<post_id>\d+)/edit$', post_edit),
    url(r'^(?P<post_id>\d+)/delete$', post_delete)
]
