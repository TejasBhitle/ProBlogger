from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse


from .models import Post
from .forms import PostForm

# Create your views here.


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "title": "Post Lists",
        "post_list": queryset
    }
    return render(request, "post_list.html", context)


def post_create(request):
    form = PostForm(request.POST or None)  # so that null fields dont pass through
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    context = {
        "form": form,
    }
    return render(request, "post_create_form.html", context)


def post_detail(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    context ={
        "post": instance
    }
    return render(request, "post_detail.html", context)
