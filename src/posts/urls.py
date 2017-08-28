from django.conf.urls import url

from .views import (post_list, post_create, post_detail,post_edit)

urlpatterns = [
    url(r'^$', post_list),
    url(r'^create/$', post_create),
    url(r'^(?P<post_id>\d+)/$', post_detail),
    url(r'^(?P<post_id>\d+)/edit$', post_edit)
]