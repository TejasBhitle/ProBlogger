from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin) :

    # to display columns
    list_display = ["title", "content", "updated", "created"]

    # to display links
    list_display_links = ["updated"]

    list_editable = ["title"]

    list_filter = ["created", "updated"]

    search_fields = ["title", "content"]


# register model in admin
admin.site.register(Post, PostModelAdmin)