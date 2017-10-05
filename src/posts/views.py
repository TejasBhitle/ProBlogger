from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from urllib import quote_plus

from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm
from comment.models import Comment
from comment.forms import CommentForm
# Create your views here.


def post_list(request):
    queryset_list = Post.objects.all().order_by("-created")

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

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
        "page_request_var": page_request_var
    }
    return render(request, "post_list.html", context)


def my_post_list(request):
    if request.user.is_authenticated():
        queryset_list = Post.objects.filter(user=request.user).order_by("-created")

        query = request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()

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
            "page_request_var": page_request_var
        }
        return render(request, "post_list.html", context)
    else:
        return redirect("/user/login/")


@login_required(login_url='/user/login/')
def post_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #    raise Http404
    form = PostForm(request.POST or None, request.FILES or None)  # so that null fields dont pass through
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, post_id):
    instance = get_object_or_404(Post, id=post_id)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_queryset = Comment.objects.filter(id=parent_id)
            if parent_queryset.exists() and parent_queryset.count() == 1:
                parent_obj = parent_queryset.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    # method defined in comment/models.py
    comments = Comment.objects.filter_by_instance(instance)

    context ={
        "post": instance,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "post_detail.html", context)


@login_required(login_url='/user/login/')
def post_edit(request, post_id=None):
    instance = get_object_or_404(Post, id=post_id)
    if not request.user == instance.user:
        return HttpResponse("<h1>You don't have permissions to do this.<h1/>")
    share_string = quote_plus(instance.content)

    # so that null fields do not pass through
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "share_string": share_string,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


@login_required(login_url='/user/login/')
def post_delete(request, post_id=None):
    instance = get_object_or_404(Post, id=post_id)
    if not request.user == instance.user:
        return HttpResponse("<h1>You don't have permissions to do this.<h1/>")
    instance.delete()
    return redirect("posts:list")
