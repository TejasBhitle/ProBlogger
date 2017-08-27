from django.conf.urls import url

from .views import (post_list, post_create, post_detail)

urlpatterns = [
    url(r'^$', post_list),
    url(r'^create/$', post_create),
    url(r'^detail/(?P<post_id>\d+)/$', post_detail)
]