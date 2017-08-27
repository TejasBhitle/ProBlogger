from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse


from .models import Post

# Create your views here.


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "title": "Post Lists",
        "post_list": queryset
    }
    return render(request, "post_list.html", context)


def post_create(request):
    return HttpResponse("<h1>Post Create</h1>")


def post_detail(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    context ={
        "post": instance
    }
    return render(request, "post_detail.html", context)
