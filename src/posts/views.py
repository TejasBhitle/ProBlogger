from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


from .models import Post
from .forms import PostForm

# Create your views here.


def post_list(request):
    queryset_list = Post.objects.all().order_by("-created")
    paginator = Paginator(queryset_list, 4)  # Show 4 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "title": "Post Lists",
        "post_list": queryset,
        "page_request_var":page_request_var
    }
    return render(request, "post_list.html", context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)  # so that null fields dont pass through
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    context ={
        "post": instance
    }
    return render(request, "post_detail.html", context)


def post_edit(request, post_id=None):
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)  # so that null fields dont pass through
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, post_id=None):
    instance = get_object_or_404(Post, id=post_id)
    instance.delete()
    return redirect("posts:list")
